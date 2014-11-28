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

# LOG_FILE = os.path.join(os.path.split(os.path.realpath("__file__"))[0],
#                         "xm.log")

SPIDER_MODULES = ['xiami.spiders']
NEWSPIDER_MODULE = 'xiami.spiders'

LOG_LEVEL = "INFO"

ITEM_PIPELINES = {
    'xiami.pipelines.XiamiPipeline': 100,
}

# redis settings
REDIS_SETTING = {
    "host": "localhost",
    "port":  6379,
    'uid_set': 'xiami_uid_set'
}
