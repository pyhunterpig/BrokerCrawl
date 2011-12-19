#! /usr/bin/env python
#coding=utf-8

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from brokercrawl.items import BrokercrawlItem
import urllib2

class SoufunSpider(BaseSpider):
    name = 'soufun_list'
    start_urls = []
    
    def totalpage(self):
        url = 'http://esf.soufun.com/agenthome/-i31'
        hxs = HtmlXPathSelector(text=urllib2.urlopen(url).read())
        total = hxs.select('//p[contains(@class,"pages")]/strong/text()').re('(\d+)')[-1]
        if total.isalnum():
            return int(total)
        else:
            return 1
        
    def start_requests(self):
        self.start_urls = ['http://esf.soufun.com/agenthome/-i3%s' %i for i in range(1,self.totalpage()+1) ]
        
        return super(SoufunSpider,self).start_requests()
        
    def parse(self, response):
        self.log('Hi, this is an list page! %s' % response.url)
        items = []
    
        hxs = HtmlXPathSelector(response)
        
        #brokers = hxs.select('//div[contains(@id,"list_") and not(@class)]')
        brokers = hxs.select('//div[@class="house"]')
        listindex = 0
        for broker in brokers:
            listindex = listindex + 1
            item = BrokercrawlItem()
            itemdata = parse_broker(broker)
            for field in item.fields:
                item[field] = itemdata.get(field,'')
            
            items.append(item)
        return items    
    
class SoufunAgentSpider(CrawlSpider):
    name = 'soufun_agent'
    allowed_domains = ['soufun.com']
    start_urls = [#'http://rent.soufun.com/rent/include/agtindex/agtindex.htm',
                  'http://esf.soufun.com/newsecond/agent/agentcenter.aspx',
                  #'http://esf.sh.soufun.com/newsecond/agent/agentcenter.aspx',
                  #'http://esf.sz.soufun.com/newsecond/agent/agentcenter.aspx',
                  #'http://esf.gz.soufun.com/newsecond/agent/agentcenter.aspx',
                  #'http://esf.tj.soufun.com/newsecond/agent/agentcenter.aspx',
                  #'http://esf.cd.soufun.com/newsecond/agent/agentcenter.aspx',
                  #'http://esf.cq.soufun.com/newsecond/agent/agentcenter.aspx',
                 ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('agent',)), callback='parse_list', follow=True),
        Rule(SgmlLinkExtractor(allow=r'/a/'), callback='parse_item', follow=False),
    )

    def parse_list(self, response):
        self.log('Hi, this is an list page! %s' % response.url)
        items = []
    
        hxs = HtmlXPathSelector(response)
        city = " ".join(hxs.select('//script/text()').re(r'cname=\s*\'(.*)\''))
        brokers = [div for div in hxs.select('//div') if div.select('div[@class="title"]')]
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
        info = hxs.select('//div[contains(@class,"intro")]')[0]
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
    title = brokerselector.select('dl/dt/p')
    if title:
        tempdict['uid'] = title[0].select('span/text()').re('(\d+)')[0]
        tempdict['site'] = title[0].select('a/@href').extract()[0].strip()
        tempdict['uname'] = title[0].select('a/text()').extract()[0].strip()        #姓名
        tempdict['mobile'] = title[2].select('strong/text()').extract()[0].strip()        #手机
        tempdict['company'] = title[1].select('span/text()').extract()[0].strip()       #所属公司
    
    tempdict['porfile'] = " ".join(brokerselector.select('dl/dd/a/img/@alt').extract())       #简介存放无法放入其他字段的个人信息
        
    return tempdict

def parse_info(infoselector):
    """
    分析店铺页面中的经纪人详细信息
    """    
    tempdict = {}
    
    return tempdict