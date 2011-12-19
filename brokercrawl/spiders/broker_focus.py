#! /usr/bin/env python
#coding=utf-8

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from brokercrawl.items import BrokercrawlItem
from scrapy.spider import BaseSpider
import urllib2

class FocusSpider(BaseSpider):
    name = 'focus_list'
    start_urls = []
    
    def totalpage(self):
        url = 'http://bj.51f.com/dianpu/'
        hxs = HtmlXPathSelector(text=urllib2.urlopen(url).read())
        total = hxs.select('//ul[@class="fr"]/li[not(@class)]/text()').re('(\d+)')[-1]
        if total.isalnum():
            return int(total)
        else:
            return 1
        
    def start_requests(self):
        self.start_urls = ['http://bj.51f.com/dianpu/p%sg0q0b0/' %i for i in range(1,self.totalpage()+1) ]
        
        return super(FocusSpider,self).start_requests()
        
    def parse(self, response):
        self.log('Hi, this is an list page! %s' % response.url)
        items = []
    
        hxs = HtmlXPathSelector(response)
        
        brokers = hxs.select('//ul[@class="user_list"]/li')
        listindex = 0
        for broker in brokers:
            listindex = listindex + 1
            item = BrokercrawlItem()
            itemdata = parse_broker(broker)
            for field in item.fields:
                item[field] = itemdata.get(field,'')
            
            items.append(item)
        return items    
    
class BrokerFocusSpider(CrawlSpider):
    name = 'broker_focus'
    allowed_domains = ['focus.cn']
    start_urls = ['http://esf.sh.focus.cn/']

    rules = (
        Rule(SgmlLinkExtractor(allow=('broker_index\.php',)), callback='parse_list', follow=True),
        Rule(SgmlLinkExtractor(allow=('broker\.php',)), callback='parse_item'),
    )

    def parse_list(self, response):
        self.log('Hi, this is an list page! %s' % response.url)
        items = []
    
        hxs = HtmlXPathSelector(response)
        brokers = hxs.select('//div[contains(@class,"col350")]')
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

    info = brokerselector.select('div[@class="info"]/p')
    tempdict['uid'] = info[0].select('strong/a/@href').re('(\d+)')[0]
    tempdict['site'] = info[0].select('strong/a/@href').extract()[0].strip()
    tempdict['uname'] = info[0].select('strong/a/text()').extract()[0].strip()        #姓名
    tempdict['mobile'] = info[0].select('b/text()').extract()[0].strip()        #手机
    tempdict['company'] = info[1].select('text()').extract()[0] + info[1].select('a/text()').extract()[0]       #所属公司
    
    tempdict['certification'] = "" #认证
    tempdict['email'] = ""      #邮件地址
    tempdict['area'] = ""          #区域
    tempdict['active'] =  ""       #活跃度
    tempdict['porfile'] = ""       #简介存放无法放入其他字段的个人信息
        
    return tempdict

def parse_info(infoselector):
    """
    分析店铺页面中的经纪人详细信息
    """    
    tempdict = {}
    
    return tempdict
