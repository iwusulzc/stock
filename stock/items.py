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
	industry = scrapy.Field()
	reg_capital = scrapy.Field()
	region = scrapy.Field()
	company_profile = scrapy.Field()
        scope_business = scrapy.Field()
        main_indicator = scrapy.Field()

	subject_matter = scrapy.Field() # 核心题材
        
class StockMainIndicator(scrapy.Item):
	period = scrapy.Field() # 报告期

	tcs = scrapy.Field()    # 总股本（Total capital stock）	
	nc = scrapy.Field()     # 流通股本（Negotiable Capital）
	
	#每股指标
	eps = scrapy.Field()    # 每股收益
	neps = scrapy.Field()   # 扣非每股收益（Non earnings per share）
	deps = scrapy.Field()   # 稀释每股收益（Diluted earnings per share）
	bvps = scrapy.Field()   # 每股净资产 (Book value of equity per share)
	cfps = scrapy.Field()   # 每股公积金 （Common fund per share）
	uddps = scrapy.Field()  # 每股未分配利润 （ Undistributed profit per share)
	ocfps = scrapy.Field()  # 每股经营现金流 （Operating cash flow per share）

	#成长能力指标
	gr = scrapy.Field()     # 营业总收入（Gross revenue）
	gp = scrapy.Field()     # 毛利润（Gross profit）
	anp = scrapy.Field()    # 归属净利润（Attribution net profit）
	nnp = scrapy.Field()    # 扣非净利润（Non net profit）
	yygtr = scrapy.Field()  # 营业总收入同比增长%（Year-on-year growth in total revenue）
	anpg = scrapy.Field()   # 归属净利润同比增长%（Attributable net profit growth）
	nnpg = scrapy.Field()   # 扣非净利润同比增长%（Non net profit growth）
	grrrc= scrapy.Field()   # 营业总收入滚动环比增长%（gross revenue rolling round comparative growth on moving base）
	anprrc = scrapy.Field() # 归属净利润滚动环比增长%
	nnprrc = scrapy.Field() # 扣非净利润滚动环比增长%

	#盈利能力指标
	wnay = scrapy.Field()   # 加权净资产收益率%（Weighted net asset yield）
	ridna = scrapy.Field()  # 摊薄净资产收益率%（Rate of income of diluted net assets）
	dacer = scrapy.Field()  # 摊薄总资产收益率%（Diluted all capital earnings rate）
	gpr = scrapy.Field()    # 毛利率%（gross profit rate）
	npr = scrapy.Field()    # 净利率%（Net Profit Ratio）
	etr = scrapy.Field()    # 实际税率%（effective tax rate）

	#盈利质量指标
	rrpr = scrapy.Field()   # 预收款/营业收入比（Revenue ratio of pre receivable）
	scfrr = scrapy.Field()  # 销售现金流/营业收入比（Sales cash flow revenue ratio）
	oircf = scrapy.Field()  # 经营现金流/营业收入（Operating income ratio of cash flow）

	#运营能力指标
	ttc = scrapy.Field()    # 总资产周转率(次)（turnover of total capital)
	dso = scrapy.Field()    # 应收账款周转天数(天)（Days sales outstanding）
	dii = scrapy.Field()    # 存货周转天数(天)（Days in Inventory）

	#财务风险指标
	alr = scrapy.Field()    # 资产负债率%（asset liability ratio)
	tlrcl = scrapy.Field()  # 流动负债/总负债(%)（Total liabilities ratio of current liabilities）
	lr = scrapy.Field()     # 流动比率（liquidity ratio）
	qr = scrapy.Field()     # 速动比率（quick ratio）
