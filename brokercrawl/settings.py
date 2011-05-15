#! /usr/bin/env python
#coding=utf-8
# Scrapy settings for brokercrawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'Mozilla'
BOT_VERSION = '5.0(X11; U; Linux i686; zh-CN; rv:1.9.1.7) Gecko/20100106 Ubuntu/9.10(karmic) Firefox/3.5.7'

SPIDER_MODULES = ['brokercrawl.spiders']
NEWSPIDER_MODULE = 'brokercrawl.spiders'
DEFAULT_ITEM_CLASS = 'brokercrawl.items.BrokercrawlItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = ['brokercrawl.pipelines.BrokercrawlPipeline']