# -*- coding: utf-8 -*-
import re
import random
import time
import redis
import scrapy
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
from scrapy import log

from xiami.tools.userpage_info import BASIC_PARSE_INFOS
from xiami.settings import REDIS_SERVER, OPEN_SET, CLOSED_SET, N_USERS_PER_ROUND
from xiami.tools.agents import ALL_AGENTS
from xiami.get_info import XiamiInfo


class XmSpider(scrapy.Spider):
    name = "xm"
    handle_httpstatus_list = [403]
    allowed_domains = ["xiami.com"]

    def __init__(self, *a, **kw):
        super(XmSpider, self).__init__(*a, **kw)
        # init redis commection
        self.r = redis.StrictRedis(**REDIS_SERVER)
        self.pipe = self.r.pipeline()

    def start_requests(self):
        # jump
        yield scrapy.Request(url="http://www.xiami.com",
                             headers={'User-Agent': random.choice(ALL_AGENTS)},
                             callback=self.gen_uids)

    def gen_uids(self, response):
        try:
            for i in range(N_USERS_PER_ROUND):
                self.pipe.spop(OPEN_SET)
            uids_pop = self.pipe.execute()
            self.pipe.delete("xiami_uid_temp")
            for x in uids_pop:
                self.pipe.sadd("xiami_uid_temp", x)
            self.pipe.execute()
            self.pipe.sdiff("xiami_uid_temp", CLOSED_SET)
            uids = self.pipe.execute()[0]
        except Exception, e:
            print e
            log.msg(e, "ERROER")
            raise CloseSpider("Something went wrong with Redis")

        for uid in uids:
            if uid == 'None':
                log.msg("Get nothing in OPEN_SET! Perhaps OPEN_SET is empty!",
                        log.WARNING)
                continue
            # parse user's basic info
            yield scrapy.Request(url="http://www.xiami.com/u/" + uid,
                                 headers={"User-Agent": random.choice(ALL_AGENTS),
                                          "Referer": None},
                                 callback=self.user_info,
                                 meta={"uid": uid,
                                       'cookiejar': int(uid)})
            # parse user's relations to songs, artists, collections, other users
            for parse_type, parse_info in BASIC_PARSE_INFOS.iteritems():
                yield scrapy.Request(url=parse_info["url"].format(uid=uid),
                                     headers={"User-Agent": random.choice(ALL_AGENTS),
                                              "Referer": None},
                                     callback=self.parse_page,
                                     meta={"type": parse_type,
                                           "n_per_page": parse_info["n_items_per_page"],
                                           "uid": uid,
                                           'cookiejar': int(uid)-1})

        # next round
        yield scrapy.Request(url="http://www.xiami.com",
                             headers={'User-Agent': random.choice(ALL_AGENTS)},
                             callback=self.gen_uids,
                             dont_filter=True)


    def user_info(self, response):
        if response.status == 403:
            log.msg("403 error! maybe the server reject the request from:" + response.url, log.INFO)
        else:
            user_info = XiamiInfo(response.body)
            user_item = user_info.get_item("user_info")
            user_item['uid'] = response.meta['uid']
            user_item['item_type'] = 'user_info'
            yield user_item

    def parse_page(self, response):
        """
        get the page info, then request for each page
        """
        if response.status == 403:
            log.msg("403 error! maybe the server reject the request from:" + response.url, log.INFO)
        else:
            soup = BeautifulSoup(response.body)
            count_info = soup.find('div', 'all_page')
            if not count_info:
                # no page split info, just parse current page
                lib = XiamiInfo(response.body)
                lib_items = lib.get_item(response.meta['type'])
                lib_items['uid'] = response.meta['uid']
                lib_items['item_type'] = response.meta['type']
                yield lib_items
            else:
                pattern = re.compile(u'共' + r'(\d+)' + u'条')
                counts = int(pattern.search(count_info.text).group(1))
                n_items_perpage = response.meta['n_per_page']
                for i in range(1, (counts - 1) / n_items_perpage + 2):
                    yield scrapy.Request(url=response.url + "/" + str(i),
                                         headers={'User-Agent': random.choice(ALL_AGENTS),
                                                  'Referer': None},
                                         callback=self.get_item,
                                         meta={"type": response.meta["type"],
                                               "uid": response.meta["uid"],
                                               'cookiejar': int(response.meta["uid"]) + i
                                         })

    def get_item(self, response):
        if response.status == 403:
            log.msg("403 error! maybe the server reject the request from:" + response.url, log.INFO)
        else:
            lib = XiamiInfo(response.body)
            lib_items = lib.get_item(response.meta['type'])
            lib_items['uid'] = response.meta['uid']
            lib_items['item_type'] = response.meta['type']
            lib_items['crawl_time'] = int(time.time())
            yield lib_items

