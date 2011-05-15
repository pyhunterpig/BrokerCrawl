#! /usr/bin/env python
#coding=utf-8

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from brokercrawl.items import BrokercrawlItem

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
    title = brokerselector.select('div[@class="title"]')
    if title:
        title = title[0]
        tempdict['site'] = " ".join(title.select('dl/dd/strong/a/@href').extract())
        tempdict['uname'] = " ".join(title.select('dl/dd/strong/a/text()').re(r'\s*(.*)\r'))          #姓名
        tempdict['mobile'] = " ".join(title.select('dl/dd[contains(@class,"floatr")]/strong/text()').re(r'\s*(.*)\r'))        #手机
        tempdict['company'] = " ".join(title.select('dl/dd[@class="floatr marr13 wid50"]/text()').re(r'\s*(.*)\r'))        #所属公司
        tempdict['lastlogin'] = " ".join(title.select('dl/dd[@class="floatr marr13"]/text()').re(r'\s*(.*)\r'))     #上次登录时间
    info = brokerselector.select('div/div[@class="floatl wid100"]')
    if info:
        info = info[0]
        tempdict['uid'] = " ".join(info.select('dl/dd[@class="floatl mart10"]/text()').re(r'\s*(.*)&'))          #ID编号
        tempdict['certification'] = " ".join(info.select('dl/dd[@class="fontm"]/img/@alt').re(r'\s*(.*)')) #认证
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