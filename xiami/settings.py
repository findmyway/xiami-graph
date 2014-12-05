# -*- coding: utf-8 -*-
import os

# Scrapy settings for xiami project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'xiami'

LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(os.path.split(os.path.realpath("__file__"))[0],
                        "xm.log")


DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
#CONCURRENT_REQUESTS = 100
#CONCURRENT_REQUESTS_PER_IP = 100
#CONCURRENT_ITEMS = 300

SPIDER_MODULES = ['xiami.spiders']
NEWSPIDER_MODULE = 'xiami.spiders'


ITEM_PIPELINES = {
    'xiami.pipelines.RedisStorePipeline': 100,
    'xiami.pipelines.UserPipeline': 150,
}


# redis settings
REDIS_SERVER= {
    "host": "172.18.32.200",
    "port": 10000,
    "db": 0
}
OPEN_SET = "xiami_unparsed_users"
CLOSED_SET = "xiami_parsed_users"
ITEM_LIST = "xiami_items"
N_USERS_PER_ROUND = 10   # parse n users per round
