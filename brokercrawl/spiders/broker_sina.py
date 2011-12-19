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
    start_urls = [
#                    'http://bj.esf.sina.com.cn/agent/',
#                  'http://sh.esf.sina.com.cn/agent/'
                  'http://tj.esf.sina.com.cn/agent/',
#                  'http://sjz.esf.sina.com.cn/agent/',
                 ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('agent',)), follow=True, callback='parse_list'),
        Rule(SgmlLinkExtractor(allow=('shop',)),  callback='parse_item'),
    )

    def parse_list(self, response):
        self.log('Hi, this is an list page! %s' % response.url)
        items = []
    
        hxs = HtmlXPathSelector(response)
        brokers = hxs.select('//ul[contains(@class,"brok_list")]/li/dl[contains(@class, "agent")]')
        for broker in brokers:
            item = BrokercrawlItem()
#            itemdata = parse_broker(broker)
#            for field in item.fields:
#                item[field] = itemdata.get(field,'')
            item['site'] = broker.select('dt/a/@href').extract()[0] + ' '
#            item['site'] = ''
            item['uid'] = broker.select('dt/a/@href').re('(\d+)')[0]
            item['uname'] = broker.select('dt/a/b/text()').extract()[0]
            item['mobile'] = broker.select('dd/span[contains(@class, "highlight")]/text()').extract()[0]
#            item['email'] = ''
#            item['city'] = ''
            item['company'] = broker.select('dd/text()').extract()[1].split(u'\uff1a')[1]
            area = broker.select('dd/a/text()').extract()[0]
            area = area + ' '
            area = area + broker.select('dd/a/text()').extract()[1]
            item['area'] = area
            item['active'] = broker.select('dt/img/@title').extract()[0].split(u': ')[1]
#            item['active'] = ''
#            item['lastlogin'] = ''     #上次登录时间
#            item['porfile'] = ''      #简介存放无法放入其他字段的个人信息
#            item['certification'] = '' #认证
            
            items.append(item)
        return items
    
    def parse_item(self, response):
        self.log('Hi, this is an shop page! %s' % response.url)
        
        hxs = HtmlXPathSelector(response)
        info = hxs.select('//div[contains(@class, "bd")]/div[contains(@class, "ag_pt02 wrapfix")]/div[contains(@class, "ag02t")]/ul/li')
        item = BrokercrawlItem()
        infodata = parse_info(info)
        for field in item.fields:
            item[field] = infodata.get(field,'')
            item['uid'] = hxs.select('//div[contains(@class, "signboard")]/ul[contains(@class, "agentNav")]/li[contains(@class, "hover")]/a/@href').extract()[0].split(u'/')[2]
        return item    

def parse_broker(brokerselector):
    """
    分析列表页中的经纪人概要信息
    """
    tempdict = []
    
    return tempdict

def parse_info(infoselector):
    """
    分析店铺页面中的经纪人详细信息
    """    
    tempdict = {}
    tempdict['uname'] = infoselector[0].select('b/text()').extract()[0]
    tempdict['active'] = infoselector[0].select('img/@title').extract()[0].split(' ')[1]
    certification = infoselector[1].select('img/@title').extract()[0]
    if certification == u'认证通过':
        tempdict['certification'] = u'身份' + certification
    else:
        tempdict['certification'] = u'身份' + certification
    area = infoselector[2].select('a/text()').extract()[0]
    area = area + ' '
    tempdict['area'] = area + infoselector[2].select('a/text()').extract()[1]
    tempdict['mobile'] = infoselector[3].select('text()').extract()[0]
    tempdict['company'] = infoselector[4].select('text()').extract()[0]
    
    return tempdict
