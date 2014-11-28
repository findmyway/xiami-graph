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

LOG_FILE = os.path.join(os.path.split(os.path.realpath("__file__"))[0],
                        "xm.log")

SPIDER_MODULES = ['xiami.spiders']
NEWSPIDER_MODULE = 'xiami.spiders'
