# -*- coding: utf-8 -*-
import re
import random

import scrapy
from bs4 import BeautifulSoup

from xiami.tools.userpage_info import BASIC_PARSE_INFOS

from xiami.tools.agents import ALL_AGENTS
from xiami.get_info import XiamiInfo


class XmSpider(scrapy.Spider):
    name = "xm"
    allowed_domains = ["xiami.com"]

    def start_requests(self):
        # jump
        yield scrapy.Request(url="http://www.xiami.com",
                             headers={'User-Agent': random.choice(ALL_AGENTS)},
                             callback=self.gen_uids)

    def gen_uids(self, response):
        uids = ["874999"]
        for uid in uids:
            # parse user's basic info
            yield scrapy.Request(url="http://www.xiami.com/u/" + uid,
                                 headers={
                                     "User-Agent": random.choice(ALL_AGENTS),
                                     "Referer": None
                                 },
                                 callback=self.user_info,
                                 meta={"uid": uid}
            )
            # parse user's relations to songs, artists, collections, other users
            for parse_type, parse_info in BASIC_PARSE_INFOS.iteritems():
                yield scrapy.Request(url=parse_info["url"].format(uid=uid),
                                     headers={
                                         "User-Agent": random.choice(ALL_AGENTS),
                                         "Referer": None
                                     },
                                     callback=self.parse_page,
                                     meta={"type": parse_type,
                                           "n_per_page": parse_info["n_items_per_page"],
                                           "uid": uid
                                     }
                )

    def user_info(self, response):
        user_info = XiamiInfo(response.body)
        user_item = user_info.get_item("user_info")
        user_item['uid'] = response.meta['uid']
        user_item['item_type'] = 'user_info'
        yield user_item

    def parse_page(self, response):
        """
        get the page info, then request for each page
        """
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
                                     headers={
                                         'User-Agent': random.choice(ALL_AGENTS),
                                         'Referer': None
                                     },
                                     callback=self.get_item,
                                     meta={"type": response.meta["type"],
                                           "uid": response.meta["uid"]})

    def get_item(self, response):
        lib = XiamiInfo(response.body)
        lib_items = lib.get_item(response.meta['type'])
        lib_items['uid'] = response.meta['uid']
        lib_items['item_type'] = response.meta['type']
        yield lib_items
