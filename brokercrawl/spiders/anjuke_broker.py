#! /usr/bin/env python
#coding=utf-8

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from brokercrawl.items import BrokercrawlItem

class AnjukeBrokerSpider(CrawlSpider):
    name = 'anjuke_broker'
    allowed_domains = ['anjuke.com']
    start_urls = ['http://beijing.anjuke.com/v2/tycoon/',
                 'http://tianjin.anjuke.com/v2/tycoon/',
                 'http://shanghai.anjuke.com/v2/tycoon/',
                 'http://sjz.anjuke.com/v2/tycoon/',
                 'http://hangzhou.anjuke.com/',
                 ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('tycoon',)), follow=True, callback='parse_list'),
        Rule(SgmlLinkExtractor(allow=('shop\.php', )), callback='parse_item'),
        
    )
    
    def parse_list(self, response):
        self.log('Hi, this is an list page! %s' % response.url)
        items = []
    
        hxs = HtmlXPathSelector(response)
        city = hxs.select('//div[@class="cur_city"]/strong/text()')[0].extract()
        brokers = hxs.select('//td[contains(@class,"coln_2")]')
        for broker in brokers:
            item = BrokercrawlItem()
            itemdata = parse_broker(broker)
            for field in item.fields:
                item[field] = itemdata.get(field,'')
            item['city'] = city
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
        item['uid'] = response.url.split('/')[-1]
        
        return item    

def parse_broker(brokerselector):
    """
    分析列表页中的经纪人概要信息
    """
    tempdict = {}
    tempdict['uid'] = brokerselector.select('div/a/@href').re('(\d+)')[0]
    tempdict['site'] = brokerselector.select('div/a/@href').extract()[0]
    tempdict['uname'] = brokerselector.select('div/a/text()').extract()[0]
    tempdict['mobile'] = brokerselector.select('div[@class="divUserMobile"]/text()').re('(\d+)')[0]
    tempdict['company'] = brokerselector.select('div[@class="divCompanyStore"]/text()').extract()[0].split(u'\uff1a')[1]
    tempdict['area'] = brokerselector.select('div[@class="divArea"]/text()').extract()[0].split(u'\uff1a')[1]
    tempdict['active'] = brokerselector.select('div[@class="divLoginStates"]/span/text()').extract()[0]
    
    return tempdict

def parse_info(infoselector):
    """
    分析店铺页面中的经纪人详细信息
    """    
    tempdict = {}
    tempdict['porfile'] = infoselector.extract()    
    return tempdict

