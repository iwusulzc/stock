# -*- coding: utf-8 -*-
import re
import sys
import scrapy
from scrapy.loader import ItemLoader
from stock.items import *
from scrapy_splash import SplashRequest

class EastmoneySpider(scrapy.Spider):
	name = "eastmoney"
	allowed_domains = ["eastmoney.com"]
	start_urls = (
			'http://quote.eastmoney.com/stock_list.html',
			)

	'''
	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url, self.parse, args={'wait': 10})
	'''

	def parse(self, response):
		#stockListLoader = ItemLoader(item = StockListItem, response = response)

		sh = response.xpath('//div[@id="quotesearch"]/div[@class="sltito"]/a/text()').extract()[0]
		sz = response.xpath('//div[@id="quotesearch"]/div[@class="sltito"]/a/text()').extract()[1]

		stock_ul = response.xpath('//div[@id="quotesearch"]/ul')

		for stock in stock_ul:
			stock_name_list = stock.xpath('li/a/text()').extract()
			stock_url_list = stock.xpath('li/a/@href').extract()
			
			# TODO: Unmatch ???
			stock_list = zip(stock_name_list, stock_url_list)
			if len(stock_list) != len(stock_name_list):
				self.logger.error("stock name url missed")
	 
			stock_code_pat = re.compile('\((.*)\)')

			for name, url in stock_list:
				stockListItem = StockListItem()

				stockListItem['exchange'] = sh
				stockListItem['name'] = name.split('(')[0]
				stockListItem['code'] = stock_code_pat.findall(name)
				stockListItem['url'] = url
				
				#yield response.follow(url, callback = self.parse_stock_page)
				yield SplashRequest(url, callback = self.parse_stock_page, args={'wait': 20})
			
	def parse_stock_page(self, response):
		f10_block = response.xpath('//div[@class="qphox"]/div[@class="hqrls"]/div[@class="cells"]')
		
		if f10_block:
				#“操盘必读”菜单
				cpbd_url = f10_block[0].xpath('a/@href')[0].extract()	

				if cpbd_url:
						# yield response.follow(cpbd_url, callback = self.parse_cpbd_page)	
						yield SplashRequest(cpbd_url, callback = self.parse_cpbd_page, args={'wait': 20})
		else:
			self.logger.error("f10 block url get failure")

	def parse_cpbd_page(self, response):
		stockBaseInfo = StockBaseInfo()
	
		stockBaseInfo['name'] = response.xpath('//*[@id="hq_1"]/text()').extract()[0]
		stockBaseInfo['code'] = response.xpath('//div[@class="main"]/div/div[@class="qphox"]/div[@class="sckifbox"]/div[@class="scklox"]/div[@class="cnt"]/p[@class="key"]/a/text()').extract()[0]

		# 最新指标表格提取
		tables = response.xpath('//div[@id="zxzbtable"]/table')
		for table in tables:
			trs = table.xpath('tbody/tr')
			for tr in trs:
				th = tr.xpath('th[@class="tips-fieldname-Left"]')
				td = tr.xpath('td[@class="tips-data-Left"]')

				if not th or not td:
					self.logger.error("%s: get stock base info", sys._getframe().f_code.co_name)

				for _th, _td in zip(th, td):
					title = _th.xpath('span/text()').extract()
					value = _td.xpath('span/text()').extract()

					if title[0] == u"基本每股收益(元)":
						stockBaseInfo['eps'] = value[0]
					elif title[0] == u"扣非每股收益(元)":
						stockBaseInfo['neps'] = value[0]
					elif title[0] == u"稀释每股收益(元)":
						stockBaseInfo['deps'] = value[0]
					elif title[0] == u"每股净资产(元)":
						stockBaseInfo['bvps'] = value[0]
					elif title[0] == u"每股公积金(元)":
						stockBaseInfo['cfps'] = value[0]
					elif title[0] == u"每股未分配利润(元)":
						stockBaseInfo['uddps'] = value[0]
					elif title[0] == u"每股经营现金流(元)":
						stockBaseInfo['ocfps'] = value[0]
					elif title[0] == u"总股本(万股)":
						stockBaseInfo['tcs'] = value[0]
					elif title[0] == u"流通股本(万股)":
						stockBaseInfo['nc'] = value[0]
					elif title[0] == u"加权净资产收益率(%)":
						stockBaseInfo['wnay'] = value[0]
					elif title[0] == u"营业总收入(元)":
						stockBaseInfo['gr'] = value[0]
					elif title[0] == u"归属净利润(元)":
						stockBaseInfo['anp'] = value[0]
					elif title[0] == u"扣非净利润(元)":
						stockBaseInfo['nnp'] = value[0]
					elif title[0] == u"毛利率(%)":
						stockBaseInfo['gir'] = value[0]
					elif title[0] == u"营业总收入滚动环比增长(%)":
						stockBaseInfo['grrrc'] = value[0]
					elif title[0] == u"归属净利润滚动环比增长(%)":
						stockBaseInfo['anprrc'] = value[0]
					elif title[0] == u"扣非净利润滚动环比增长(%)":
						stockBaseInfo['nnprrc'] = value[0]
					elif title[0] == u"资产负债率(%)":
						stockBaseInfo['alr'] = value[0]
					elif title[0] == u"营业总收入同比增长(%)":
						stockBaseInfo['yygtr'] = value[0]
					elif title[0] == u"归属净利润同比增长(%)":
						stockBaseInfo['anpg'] = value[0]
					elif title[0] == u"扣非净利润同比增长(%)":
						stockBaseInfo['nnpg'] = value[0]
					else:
						self.logger.warning("%s: Unknow item, %s = %s", sys._getframe().f_code.co_name, name, value)

		# 核心题材
		sms = response.xpath('//div[@class="section"]/div/div[@class="summary"]/p')
		sm_content = ""

		for sm in sms: 
			content = sm.xpath('./text()').extract()
			#content = re.sub(u'(要点)<.*>', '', _content)
			for c in content:
				sm_content += c
			
			sm_content += '\n'
	
		stockBaseInfo['sm'] = sm_content

		if stockBaseInfo:
			yield stockBaseInfo

	def parse_eastmoney_data_page(self, response):
		pass

	def data_menu_url_get(self, response):
		data_menu = response.xpath('//div[@class="nav"]/div[@class="navlist"]/ul[@class="mu101"]/li')[1]
		data_menu_url = data_menu.css('a::attr(href)')[3].extract()
		if data_menu_url:
			self.logger.debug('data menu href: %s', data_menu_url)
		return data_menu_url
