#! /usr/bin/env python
#coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BrokercrawlItem(Item):
    # define the fields for your item here like:
    # name = Field()
    site = Field()          #网站
    uid = Field()           #ID编号
    uname = Field()         #姓名
    mobile = Field()        #手机
    email = Field()         #邮件地址
    city = Field()          #城市
    company = Field()       #所属公司
    area = Field()          #区域
    active = Field()        #活跃度
    lastlogin = Field()     #上次登录时间
    porfile = Field()       #简介存放无法放入其他字段的个人信息
    certification = Field() #认证
