# -*- coding: utf-8 -*-
import re
import random
import scrapy
from bs4 import BeautifulSoup
from xiami.tools.agents import ALL_AGENTS
from xiami.get_info import XiamiInfo


class XmSpider(scrapy.Spider):
    name = "xm"
    user_url = "http://www.xiami.com/u/{uid}"
    libsong_url = "http://www.xiami.com/space/lib-song/u/{uid}/page"
    unlibsong_url = "http://www.xiami.com/space/unlib-song/u/{uid}/page"
    libalbum_url = "http://www.xiami.com/space/lib-album/u/{uid}/page"
    libartist_url = "http://www.xiami.com/space/lib-artist/u/{uid}/page"
    song_weekrank_url = "http://www.xiami.com/space/charts/u/{uid}/c/song/t/week/page"
    song_totalrank_url = "http://www.xiami.com/space/charts/u/{uid}/c/song/t/all/page"
    album_weekrank_url = "http://www.xiami.com/space/charts/u/{uid}/c/album/t/week/page"
    album_totalrank_url = "http://www.xiami.com/space/charts/u/{uid}/c/album/t/all/page"
    artist_totalrank_url = "http://www.xiami.com/space/charts/u/{uid}/c/artist/t/all/page"
    artist_weekrank_url = "http://www.xiami.com/space/charts/u/{uid}/c/artist/t/week/page"
    collect_url = "http://www.xiami.com/space/collect/u/{uid}/order/1/p/1/page"
    collect_fav_url = "http://www.xiami.com/space/collect-fav/u/{uid}/order//page"

    allowed_domains = ["xiami.com"]

    current_uid = "8539366"

    def start_requests(self):
        yield scrapy.Request(url=self.user_url.format(uid=self.current_uid),
                             headers={'User-Agent': random.choice(ALL_AGENTS)},
                             callback=self.parse_user)

    def parse_user(self, response):
        # step1: get user info
        # user_info = XiamiInfo(response.body)
        # user_item = user_info.get_item("user_info")
        # user_item['uid'] = self.current_uid
        # user_item['item_type'] = 'user_info'

        # yield user_item
        #
        # step2: get lib_songs
        # yield scrapy.Request(url=self.libsong_url.format(uid=self.current_uid),
        #                      headers={
        #                          'User-Agent': random.choice(ALL_AGENTS),
        #                          'Referer': None
        #                      },
        #                      callback=self.parse_page,
        #                      meta={"type": "lib_song",
        #                            "n_per_page": 25})

        #
        # step3: get unlib_songs
        # yield scrapy.Request(url=self.unlibsong_url.format(uid=self.current_uid),
        #                       headers={
        #                           'User-Agent': random.choice(ALL_AGENTS),
        #                           'Referer': None
        #                       },
        #                     callback=self.parse_page,
        #                     meta={"type": "unlib_song", "n_per_page": 25})

        # step4: get lib_albums
        # yield scrapy.Request(url=self.libalbum_url.format(uid=self.current_uid),
        #                       headers={
        #                           'User-Agent': random.choice(ALL_AGENTS),
        #                           'Referer': None
        #                       },
        # callback=self.parse_page,
        # meta={"type": "lib_album", "n_per_page": 15})

        # step5: get lib_artists
        # yield scrapy.Request(url=self.libartist_url.format(uid=self.current_uid),
        #                       headers={
        #                           'User-Agent': random.choice(ALL_AGENTS),
        #                           'Referer': None
        #                       },
        # callback=self.parse_page,
        # meta={"type": "lib_artist", "n_per_page": 15})

        # step:6 get song_weekrank
        # yield scrapy.Request(url=self.song_weekrank_url.format(uid=self.current_uid),
        #                   headers={
        #                       'User-Agent': random.choice(ALL_AGENTS),
        #                       'Referer': None
        #                   },
        #                      callback=self.parse_page,
        #                      meta={"type": "song_weekrank", "n_per_page": 20})

        # step:7 get song_totalrank
        # yield scrapy.Request(url=self.song_totalrank_url.format(uid=self.current_uid),
        #                      headers={
        #                          'User-Agent': random.choice(ALL_AGENTS),
        #                          'Referer': None
        #                      },
        #                      callback=self.parse_page,
        #                      meta={"type": "song_totalrank", "n_per_page": 20})

        # step:8 get album_weekrank
        # yield scrapy.Request(url=self.album_weekrank_url.format(uid=self.current_uid),
        #                      headers={
        #                          'User-Agent': random.choice(ALL_AGENTS),
        #                          'Referer': None
        #                      },
        #                      callback=self.parse_page,
        #                      meta={"type": "album_weeklrank", "n_per_page": 20})

        # step:9 get album_totalrank
        # yield scrapy.Request(url=self.album_totalrank_url.format(uid=self.current_uid),
        #                      headers={
        #                          'User-Agent': random.choice(ALL_AGENTS),
        #                          'Referer': None
        #                      },
        #                      callback=self.parse_page,
        #                      meta={"type": "album_totalrank", "n_per_page": 20})

        # step:10 get artist_weekrank
        # yield scrapy.Request(url=self.artist_weekrank_url.format(uid=self.current_uid),
        #                      headers={
        #                          'User-Agent': random.choice(ALL_AGENTS),
        #                          'Referer': None
        #                      },
        #                      callback=self.parse_page,
        #                      meta={"type": "artist_weekrank", "n_per_page": 20})

        # step:11 get artist_totalrank
        # yield scrapy.Request(url=self.artist_totalrank_url.format(uid=self.current_uid),
        #                      headers={
        #                          'User-Agent': random.choice(ALL_AGENTS),
        #                          'Referer': None
        #                      },
        #                      callback=self.parse_page,
        #                      meta={"type": "artist_totalrank", "n_per_page": 20})

        # step:12 get collect
        # yield scrapy.Request(url=self.collect_url.format(uid=self.current_uid),
        #                      headers={
        #                          'User-Agent': random.choice(ALL_AGENTS),
        #                          'Referer': None
        #                      },
        #                      callback=self.parse_page,
        #                      meta={"type": "collect", "n_per_page": 12})

        # step:13 get collect_fav
        yield scrapy.Request(url=self.collect_fav_url.format(uid=self.current_uid),
                             headers={
                                 'User-Agent': random.choice(ALL_AGENTS),
                                 'Referer': None
                             },
                             callback=self.parse_page,
                             meta={"type": "collect_fav", "n_per_page": 12})



    def parse_page(self, response):
        soup = BeautifulSoup(response.body)
        count_info = soup.find('div', 'all_page')
        if not count_info:
            # 没有分页信息, 则表明只有一页,解析当前页即可
            lib = XiamiInfo(response.body)
            lib_items = lib.get_item(response.meta['type'])
            lib_items['uid'] = self.current_uid
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
                                     meta={"type": response.meta["type"]})

    def get_item(self, response):
        lib = XiamiInfo(response.body)
        lib_items = lib.get_item(response.meta['type'])
        lib_items['uid'] = self.current_uid
        lib_items['item_type'] = response.meta['type']
        yield lib_items
