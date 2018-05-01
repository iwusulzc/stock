# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import csv 
from scrapy.exceptions import DropItem

class StockPipeline(object):
    def process_item(self, item, spider):
        return item

class StockBaseInfoPipeline(object):
	def __init__(self):
		self.maptable = {\
			'report_period' : u'报告期', \
			'esp' : u'每股收益', \
			'neps' : u'扣非每股收益', \
			'deps' : u'稀释每股收益', \
			'bvps' : u'每股净资产', \
			'cfps' : u'每股公积金', \
			'uddps' : u'每股未分配利润', \
			'ocfps' : u'每股经营现金流', \
			'tcs' : u'总股本', \
			'nc' : u'流通股本', \
			'wnay' : u'加权净资产收益率', \
			'gr' : u'营业总收入', \
			'anp' : u'归属净利润', \
			'nnp' : u'扣非净利润', \
			'gir' : u'毛利率', \
			'grrrc' : u'营业总收入滚动环比增长', \
			'anprrc' : u'归属净利润滚动环比增长', \
			'nnprrc' : u'扣非净利润滚动环比增长', \
			'alr' : u'资产负债率', \
			'yygtr' : u'营业总收入同比增长', \
			'anpg' : u'归属净利润同比增长', \
			'nnpg' : u'扣非净利润同比增长', \
			'sm' : u'核心题材'}

		self.title = (
			u'股票名菜', \
			u'股票代码', \
			u'交易所', \
			u'报告期', \
			u'每股收益', \
			u'扣非每股收益', \
			u'稀释每股收益', \
			u'每股净资产', \
			u'每股公积金', \
			u'每股未分配利润', \
			u'每股经营现金流', \
			u'总股本', \
			u'流通股本', \
			u'加权净资产收益率', \
			u'营业总收入', \
			u'归属净利润', \
			u'扣非净利润', \
			u'毛利率', \
			u'营业总收入滚动环比增长', \
			u'归属净利润滚动环比增长', \
			u'扣非净利润滚动环比增长', \
			u'资产负债率', \
			u'营业总收入同比增长', \
			u'归属净利润同比增长', \
			u'扣非净利润同比增长', \
			u'核心题材')

		self.file = open('StockBaseInfo.json', 'a+')
		self.csvwriter = csv.writer(self.file)

	def open_spider(self, spider):
		pass

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		if item.__class__.__name__ == 'StockItem0':
			line = json.dumps(dict(item)) + '\n'
			self.file.write(line)
			#self.csvwriter.writerow(dict(item).values().decode('utf-8'))
			raise DropItem("")
		else:
			return item
