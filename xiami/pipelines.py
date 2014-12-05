# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import cPickle
import redis
from scrapy import log
from scrapy.exceptions import CloseSpider

from xiami.settings import REDIS_SERVER, OPEN_SET, CLOSED_SET, ITEM_LIST


class UserPipeline(object):
    def __init__(self):
        self.r = redis.StrictRedis(**REDIS_SERVER)
        self.pipe = self.r.pipeline()

    def process_item(self, item, spider):
        if item['item_type'] in ['followings', 'fans']:
            for x in item['items']:
                self.pipe.sadd(OPEN_SET, x)
            self.pipe.sadd(CLOSED_SET, item['uid'])
            try:
                self.pipe.execute()
            except Exception, e:
                print e
                log.msg(e, log.ERROR)
                raise CloseSpider("Something went wrong with Redis")
        # return item, in case I will need more process with it
        return item


class RedisStorePipeline(object):
    def __init__(self):
        self.r = redis.StrictRedis(**REDIS_SERVER)

    def process_item(self, item, spider):
        try:
            self.r.rpush(ITEM_LIST, cPickle.dumps(item))
        except Exception, e:
            print e
            log.msg(e, log.ERROR)
            raise CloseSpider("Something went wrong with Redis")
        return item
