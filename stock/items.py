# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
	name = scrapy.Field()
	code = scrapy.Field()
	exchange = scrapy.Field()

class StockListItem(StockItem):
	url = scrapy.Field()

class StockBaseInfo(StockItem):
	report_period = scrapy.Field() # 报告期
	eps = scrapy.Field()    # 每股收益
	neps = scrapy.Field()   # 扣非每股收益（Non earnings per share）
	deps = scrapy.Field()   # 稀释每股收益（Diluted earnings per share）
	bvps = scrapy.Field()   # 每股净资产 (Book value of equity per share)
	cfps = scrapy.Field()   # 每股公积金 （Common fund per share）
	uddps = scrapy.Field()  # 每股未分配利润 （ Undistributed profit per share)
	ocfps = scrapy.Field()  # 每股经营现金流 （Operating cash flow per share）
	tcs = scrapy.Field()    # 总股本（Total capital stock）	
	nc = scrapy.Field()     # 流通股本（Negotiable Capital）

	wnay = scrapy.Field()   # 加权净资产收益率（Weighted net asset yield）
	gr = scrapy.Field()     # 营业总收入（Gross revenue）
	anp = scrapy.Field()    # 归属净利润（Attribution net profit）
	nnp = scrapy.Field()    # 扣非净利润（Non net profit）
	gir = scrapy.Field()    # 毛利率（Gross interest rate）
	grrrc= scrapy.Field()   # 营业总收入滚动环比增长（gross revenue rolling round comparative growth on moving base）
	anprrc = scrapy.Field() # 归属净利润滚动环比增长
	nnprrc = scrapy.Field() # 扣非净利润滚动环比增长
	alr = scrapy.Field()    # 资产负债率（Asset liability ratio）
	yygtr = scrapy.Field()  # 营业总收入同比增长（Year-on-year growth in total revenue）
	anpg = scrapy.Field()   # 归属净利润同比增长（Attributable net profit growth）
	nnpg = scrapy.Field()   # 扣非净利润同比增长（Non net profit growth）
	sm = scrapy.Field()	    # (subject matter)
