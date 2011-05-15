#! /usr/bin/env python
#coding=utf-8

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from brokercrawl.items import BrokercrawlItem

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
    fieldname = {'姓名':'uname',
                 '电话':'mobile',
                 '服务区域':'area',
                 '所属公司':'company',
                }
    info = brokerselector.select('div/ul[@class="jjr_description"]')
    if info:
        info = info[0]
        for li in info.select('li'):
            key = "".join(li.select('b/text()').extract())
            if key:
                key = key.encode('utf8')
                if key == '电话':
                    value = "".join(li.select('span/text()').extract())
                else:
                    value = "".join(li.select('text()').extract())
                if fieldname.has_key(key):
                    tempdict[fieldname[key]] = value
            else:
                tempdict['site'] = " ".join(li.select('a/@href').extract())
                tempdict['uid'] = " ".join(li.select('a/@href').re('(\d+)'))
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
