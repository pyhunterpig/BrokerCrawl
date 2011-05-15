#! /usr/bin/env python
#coding=utf-8

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from brokercrawl.items import BrokercrawlItem

class BrokerSinaSpider(CrawlSpider):
    name = 'broker_sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://bj.esf.sina.com.cn/agent/',
                  'http://sh.esf.sina.com.cn/agent/',
                  'http://tj.esf.sina.com.cn/agent/',
                  'http://sjz.esf.sina.com.cn/agent/',
                 ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('agent',)), follow=True, callback='parse_list'),
        Rule(SgmlLinkExtractor(allow=('shop',)),  callback='parse_item'),
    )

    def parse_list(self, response):
        self.log('Hi, this is an list page! %s' % response.url)
        items = []
    
        hxs = HtmlXPathSelector(response)
        brokers = hxs.select('//td[contains(@class,"coln_2")]')
        for broker in brokers:
            item = BrokercrawlItem()
            itemdata = parse_broker(broker)
            for field in item.fields:
                item[field] = itemdata.get(field,'')
            items.append(item)
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
