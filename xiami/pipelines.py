# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
from redis import ConnectionError
from scrapy import log
from scrapy.exceptions import CloseSpider
from xiami.settings import REDIS_SETTING as rd_setting

class XiamiPipeline(object):
    def __init__(self):
        self.r = redis.StrictRedis(host=rd_setting['host'],
                                   port=rd_setting['port'])
        self.pipe = self.r.pipeline()

    def process_item(self, item, spider):
        if item['item_type'] in ['followings', 'fans']:
            for x in item['items']:
                self.pipe.sadd(rd_setting['uid_set'], x)
            try:
                self.pipe.execute()
            except ConnectionError, e:
                print e
                log.msg("Connection to redis failed! Check it!!!", "CRITICAL")
                raise CloseSpider("Can not connect to redis")
