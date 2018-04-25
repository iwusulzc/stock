# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
	name = scrapy.Field()
	stock_code = scrapy.Field()

class StockListItem(scrapy.Item):
	exchange = scrapy.Field()
	name = scrapy.Field()
	stock_code = scrapy.Field()
	url = scrapy.Field()

class StockBaseInfo(scrapy.Item):
	eps = scrapy.Field()    # 每股收益
	neps = scrapy.Field()   # 扣非每股收益（Non earnings per share）
	deps = scrapy.Field()   # 稀释每股收益（Diluted earnings per share）
	bvps = scrapy.Field()   # 每股净资产 (Book value of equity per share)
	cfps = scrapy.Field()   # 每股公积金 （Common fund per share）
	uddps = scrapy.Field()  # 每股未分配利润 （ Undistributed profit per share)
	ocfps = scrapy.Field()  # 每股经营现金流 （Operating cash flow per share）
	tcs = scrapy.Field()    # 总股本（Total capital stock）	
	nc = scrapy.Field()     # 流通股本（Negotiable Capital）

