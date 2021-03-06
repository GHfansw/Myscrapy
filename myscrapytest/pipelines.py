# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class ZhihuPipeline(object):
    def __init__(self):
        self.filename = open("zhihu.json", "wb")

    def process_item(self, item, spider):
        if spider.name == 'zhihu2':  # 这里是哪一个爬虫的pipline的逻辑判断
            text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.filename.write(text.encode("utf-8"))
            return item
        else:
            pass

    def close_spider(self, spider):
        self.filename.close()
