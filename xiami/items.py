# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    item_type = scrapy.Field()
    uid = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    sex = scrapy.Field()
    join_time = scrapy.Field()
    n_listen = scrapy.Field()
    n_visit = scrapy.Field()
    n_followers = scrapy.Field()
    n_fans = scrapy.Field()
    n_share = scrapy.Field()

class LibItem(scrapy.Item):
    item_type = scrapy.Field()
    uid = scrapy.Field()
    items = scrapy.Field()

