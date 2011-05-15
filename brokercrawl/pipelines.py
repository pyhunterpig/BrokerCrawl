#! /usr/bin/env python
#coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise DirectException("No JSON library available. Please install"
                              " simplejson or upgrade to Python 2.6.")

class BrokercrawlPipeline(object):
    def process_item(self, item, spider):
        open('%s_%s.json' %(spider.name,item['city']),'a').write('%s\n' %json.dumps(item._values))
        
        return item
