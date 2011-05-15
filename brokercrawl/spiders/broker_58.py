#! /usr/bin/env python
#coding=utf-8

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from brokercrawl.items import BrokercrawlItem

class Broker58Spider(CrawlSpider):
    name = 'broker_58'
    allowed_domains = ['58.com']
    start_urls = ['http://bj.58.com/ershoufang/1/',
                  'http://sh.58.com/ershoufang/1/',
                 ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('pn',)), follow=True),
        Rule(SgmlLinkExtractor(allow=('x\.shtml',)), callback='parse_item'),
    )

    def parse_list(self, response):
        self.log('Hi, this is an list page! %s' % response.url)
        items = []
    
        
        return items
    
    def parse_item(self, response):
        self.log('Hi, this is an shop page! %s' % response.url)
        
        hxs = HtmlXPathSelector(response)
        info = hxs.select('//div[contains(@class,"profile")]')[0]
        item = BrokercrawlItem()
        infodata = parse_info(info)
        for field in item.fields:
            item[field] = infodata.get(field,'')
        
        return item    

def parse_broker(brokerselector):
    """
    分析列表页中的经纪人概要信息
    """
    tempdict = {}
    
    return tempdict

def parse_info(infoselector):
    """
    分析店铺页面中的经纪人详细信息
    """    
    tempdict = {}
    
    return tempdict
