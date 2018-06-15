# -*- coding: utf-8 -*-
import re
import sys
import scrapy
from scrapy.loader import ItemLoader
from stock.items import *
from scrapy_splash import SplashRequest

script = """
	function main(splash, args)
		assert(splash:go(args.url))
		assert(splash:wait(3))
		js = string.format("document.querySelectorAll('#zyzbTab li')[%d].click()", args.period)
	    splash:evaljs(js)
		assert(splash:wait(args.wait))
		return {
			 html = splash:html(),
		}
	end
	"""

class EastmoneySpider(scrapy.Spider):
	name = "eastmoney"
	allowed_domains = ["eastmoney.com"]
	start_urls = (
			'http://quote.eastmoney.com/stock_list.html',
			)

	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url, self.parse, args={'wait': 10})
	
	"""
	def start_requests(self):
		#url = "http://emweb.securities.eastmoney.com/f10_v2/OperationsRequired.aspx?type=web&code=sz000002"
		#yield SplashRequest(url, self.transfer_page, args={'wait': 10})

		urls = (
			'http://quote.eastmoney.com/sh600028.html',
			'http://quote.eastmoney.com/sz000002.html',
			)
		for url in urls:
			yield SplashRequest(url, self.parse_stock_page, args={'wait': 10})
	"""

	def parse(self, response):
		stock_match = ['00', '30', '60']

		#stockListLoader = ItemLoader(item = StockListItem, response = response)

		stock_ul = response.xpath('//div[@id="quotesearch"]/ul')
		parse_stock_nr = 0

		for stock in stock_ul:
			stock_name_list = stock.xpath('li/a/text()').extract()
			stock_url_list = stock.xpath('li/a/@href').extract()
			
			# TODO: Unmatch ???
			if len(stock_url_list) != len(stock_name_list):
				self.logger.error("stock name url missed")
	 
			stock_code_pat = re.compile('\((.*)\)')

			stock_list = zip(stock_name_list, stock_url_list)

			for name, url in stock_list:
				_name = name.split('(')[0]
				code = stock_code_pat.findall(name)[0]
				if (code[0:2] not in stock_match and code[0:3] not in stock_match):
					continue

				self.logger.info("parse %s, %s", _name, code)
				parse_stock_nr += 1

				yield SplashRequest(url, callback = self.parse_stock_page, args={'wait': 20})
		self.logger.info("parse stock number: %d", parse_stock_nr)

	def parse_stock_page(self, response):
		f10_block = response.xpath('//div[@class="qphox"]/div[@class="hqrls"]/div[@class="cells"]')
		if f10_block:
			#“操盘必读”菜单
			cpbd_url = f10_block[0].xpath('a/@href')[0].extract()
			if cpbd_url:
				yield SplashRequest(cpbd_url, callback = self.transfer_page, args={'wait': 20})
			else:
				self.logger.error("f10 block url get failure")
						
	def transfer_page(self, response):
		# 公司概况
		companySurvey_url = "http://emweb.securities.eastmoney.com"
		url = response.xpath('//li[@id="CompanySurvey"]/a/@href').extract()[0]
		
		companySurvey_url += url[2:]
		print("companySurvey_url: %s" % companySurvey_url)
		if companySurvey_url:
			yield SplashRequest(companySurvey_url, \
				callback = self.parse_company_survey_page, args={'wait': 20})
			
	# 公司概况解析
	def parse_company_survey_page(self, response):
		stockItem = StockItem()
		
		stock_kw_dict = {
			u'A股代码' : 'code',
			u'A股简称' : 'name',
			u'上市交易所' : 'exchange',
			u'所属证监会行业' : 'industry',
			u'区域' : 'region',
			u'注册资本(元)' : 'reg_capital',
			#u'公司简介' : 'company_profile',
			#u'经营范围' : 'scope_business',
			}

		# 公司概况表
		trs = response.xpath('//table[@id="Table0"]/tbody/tr')
		
		for tr in trs:
			ths = tr.xpath('th/text()').extract()
			tds = tr.xpath('td/text()').extract()
			
			for th, td in zip(ths, tds):
				title = th.strip()
				value = td.strip()
				if title not in stock_kw_dict:
					continue
				
				key = stock_kw_dict[title]

				if (key == 'reg_capital'):
					value = self.unit_convert(value)
				elif (key == 'code' and value == '--'):
					self.logger.info('stockitem code was NULL')
					return
				else:
					pass

				stockItem[key] = value

		if 'code' not in stockItem:
			self.logger.warning('stockitem base info get failure')
			print(trs)

		coreconception_url = response.xpath('//li[@id="CoreConception"]/a/@href').extract()
		if coreconception_url:
			r = SplashRequest(response.urljoin(coreconception_url[0]), \
				callback = self.parse_coreconception_page, args={'wait': 20})
			r.meta['item'] = stockItem
			yield r        

	def parse_coreconception_page(self, response):
		stockItem = response.meta['item']
		sms = response.xpath('//div[@class="summary"]/p')
		sm_content = ""

		for sm in sms:
			content = sm.xpath('./text()').extract()
			#content = re.sub(u'(要点)<.*>', '', _content)
			for c in content:
				sm_content += c

			sm_content += '\n'

		if 'subject_matter' in stockItem:
			stockItem['subject_matter'] = sm_content

		# next page: 财务分析
		financial_analysis_url = response.xpath('//li[@id="NewFinanceAnalysis"]/a/@href').extract()[0]
		r = SplashRequest(response.urljoin(financial_analysis_url), \
			callback = self.parse_financial_analysis_page, args={'wait': 20})
		r.meta['item'] = stockItem
		yield r        
		
	# 财务分析页面
	def parse_financial_analysis_page(self, response):
		stock_kw_dict = {
			u'基本每股收益(元)' : 'eps',
			u'扣非每股收益(元)' : 'neps',
			u'稀释每股收益(元)' : 'deps',
			u'每股净资产(元)' : 'bvps',
			u'每股公积金(元)' : 'cfps',
			u'每股未分配利润(元)' : 'uddps',
			u'每股经营现金流(元)' : 'ocfps',
			u'营业总收入(元)' : 'gr',
			u'毛利润(元)' : 'gp',
			u'归属净利润(元)' : 'anp',
			u'扣非净利润(元)' : 'nnp',
			u'营业总收入同比增长(%)' : 'yygtr',
			u'归属净利润同比增长(%)' : 'anpg',
			u'扣非净利润同比增长(%)' : 'nnpg',
			u'营业总收入滚动环比增长(%)' : 'grrrc',
			u'归属净利润滚动环比增长(%)' : 'anprrc',
			u'扣非净利润滚动环比增长(%)' : 'nnprrc',
			u'加权净资产收益率(%)' : 'wnay',
			u'摊薄净资产收益率(%)' : 'ridna',
			u'摊薄总资产收益率(%)' : 'dacer',
			u'毛利率(%)' : 'gpr',
			u'净利率(%)' : 'npr',
			u'实际税率(%)' : 'etr',
			u'预收款/营业收入' : 'rrpr',
			u'销售现金流/营业收入' : 'scfrr',
			u'经营现金流/营业收入' : 'oircf',
			u'总资产周转率(次)' : 'ttc',
			u'应收账款周转天数(天)' : 'dso',
			u'存货周转天数(天)' : 'dii',
			u'资产负债率(%)' : 'alr',
			u'流动负债/总负债(%)' : 'tlrcl',
			u'流动比率' : 'lr',
			u'速动比率' : 'qr',
			}

		stock_kws = {
			'eps', 'neps', 'deps', 'bvps', 'cfps', 'uddps', 'ocfps', 'gr',
			'gp', 'anp', 'nnp', 'yygtr', 'anpg', 'nnpg', 'grrrc', 'anprrc',
			'nnprrc', 'wnay', 'ridna', 'dacer', 'gpr', 'npr', 'etr', 'rrpr',
			'scfrr', 'oircf', 'ttc', 'dso', 'dii', 'alr', 'tlrcl', 'lr', 'qr',
		}

		stockItem = response.meta['item']
		for kw in stock_kws:
			stockItem[kw] = ''

		# main indicator table
		trs = response.xpath('//div[@id="report_zyzb"]/table/tbody/tr')

		#处理表头，取出报告期日期
		period_date = []
		ths = trs[0].xpath('th')

		for th in ths:
			value = th.xpath('span/text()').extract()[0]
			period_date.append(value)
		
		if not period_date:
			pass

		tds_value = []

		for tr in trs:
			# 处理表的具体内容
			tds = tr.xpath('td')

			if not tds:
				continue

			td_value = [] 

			for td in tds:
				value = td.xpath('span/text()').extract()[0]
				td_value.append(value)

			if td_value:
				tds_value.append(td_value)
				
		period_dict = {u'按报告期' : 0, u'按年度' : 1, u'按单季度' : 2}
		period = response.xpath('//ul[@id="zyzbTab"]/li[@class="current"]/text()').extract()[0].strip()

		if 'code' not in stockItem:
			self.logger.warning('stockitem not code item')

		for x in range(1, len(tds_value[0])):
			_stockItem = stockItem.copy()

			for y in range(len(tds_value)):
				key = tds_value[y][0].strip(' \n')
				if key not in stock_kw_dict:
					self.logger.warning("%s: No process key = %s", \
						sys._getframe().f_code.co_name, key)
					break
				item = stock_kw_dict[key]
				_stockItem[item] = self.unit_convert(tds_value[y][x])
			_stockItem['date'] = period_date[x]
			_stockItem['period'] = period

			yield _stockItem

		if period in period_dict:
			page = period_dict[period]

			if page == 2:
				# last page, parse next page:
				pass
			else:
				next_period = page + 1
				r = SplashRequest(response.url, \
						callback = self.parse_financial_analysis_page, endpoint='execute', \
						args={'lua_source': script, 'wait': 10, 'period': next_period})
				r.meta['item'] = stockItem
				yield r
		else:
			self.logger.error("%s: period get error(%s)", sys._getframe().f_code.co_name, period)
			# raise error info??

	# str_value format: 1234亿, 1234万亿, 1234万
	def unit_convert(self, str_value):
		unit_dict = {'万亿' : 1000000000000, '千亿' : 100000000000, '亿' : 100000000, \
					'万万' : 100000000, '千万' : 10000000, '百万' : 1000000, '十万' : 100000, '万' : 10000, '千' : 1000}
		str_value = str_value.strip(' \n')
		ret = re.search('^([-]?\d+|[-]?\d+\.\d+)$', str_value)
		if (ret is not None):
			return str_value

		ret = re.search('^([-]?\d+|[-]?\d+\.\d+)([\u4e00-\u9fa5]+)$', str_value)

		if (ret is None):
			return str_value

		value = ret.group(1)
		unit = ret.group(2)
		if (unit not in unit_dict):
			self.logger.info('Unknow unit %s', unit)
			return str_value
		else:
			return '{:.6g}'.format(float(value) * unit_dict[unit])

