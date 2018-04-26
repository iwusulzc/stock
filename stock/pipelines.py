# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class StockPipeline(object):
    def process_item(self, item, spider):
        return item

class StockBaseInfoPipeline(object):
	def open_spider(self, spider):
		self.file = open('StockBaseInfo.json', 'a+')

	def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
		print("item class name: ", item.__class__)

		if item.__class__ == 'StockBaseInfoItem':
				line = json.dumps(dict(item)) + "\n"
				self.file.write(line)
				raise DropItem("")
		else:
				return item
