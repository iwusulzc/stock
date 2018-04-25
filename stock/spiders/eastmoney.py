# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.loader import ItemLoader
from stock.items import *

class EastmoneySpider(scrapy.Spider):
	name = "eastmoney"
	allowed_domains = ["eastmoney.com"]
	start_urls = (
			#'http://www.eastmoney.com/',
			'http://quote.eastmoney.com/stock_list.html',
			)
	'''
	def parse(self, response):
		data_menu_url = self.data_menu_url_get(response)
		if data_menu_url:
			yield scrapy.Request(data_menu_url, callback=self.parse_eastmoney_data_page)
		else:
			self.logger.error('data menu url get failure')
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
				stockListItem['stock_code'] = stock_code_pat.findall(name)
				stockListItem['url'] = url
				
				yield response.follow(url, callback = self.parse_stock_page)
			
	def parse_stock_page(self, response):
		f10_block = response.xpath('//div[@class="qphox"]/div[@class="hqrls"]/div[@class="cells"]')
		
		if f10_block:
				#“操盘必读”菜单
				cpbd_url = f10_block[0].xpath('a/@href')[0].extract()	
				self.logger.debug("cpbd url: %s", cpbd_url)

				if cpbd_url:
						yield response.follow(cpbd_url, callback = self.parse_cpbd_page)	
		else:
			self.logger.error("f10 block url get failure")

	def parse_cpbd_page(self, response):
		stockBaseInfo = StockBaseInfo()
		
		tr = response.xpath('//div[@id="zxzbtable"]/table/tbody/tr')
		for i in range(1, len(tr)):
			th = tr[i].xpath('th[@class="tips-fieldname-Left"]')
			td = tr[i].xpath('td[@class="tips-data-Left"]')
			for _th, _td in zip(th, td):
				name = _th.xpath('span/text()')
				value = _td.xpath('span/text()')

				if name == u"基本每股收益(元)":
					stockBaseInfo['eps'] = value
				elif name == u"扣非每股收益(元)":
					stockBaseInfo['neps'] = value
				elif name == u"稀释每股收益(元)":
					stockBaseInfo['deps'] = value
				elif name == u"每股净资产(元)":
					stockBaseInfo['bvps'] = value
				elif name == u"每股公积金(元)":
					stockBaseInfo['cfps'] = value
				elif name == u"每股未分配利润(元)":
					stockBaseInfo['uddps'] = value
				elif name == u"每股经营现金流(元)":
					stockBaseInfo['ocfps'] = value
				elif name == u"总股本(万股)":
					stockBaseInfo['tcs'] = value
				elif name == u"流通股本(万股)":
					stockBaseInfo['nc'] = value
				else:
					self.logger.info("Unknow item, %s = %s", name, value)
		yield stockBaseInfo
	
	def parse_eastmoney_data_page(self, response):
		pass

	def data_menu_url_get(self, response):
		data_menu = response.xpath('//div[@class="nav"]/div[@class="navlist"]/ul[@class="mu101"]/li')[1]
		data_menu_url = data_menu.css('a::attr(href)')[3].extract()
		if data_menu_url:
			self.logger.debug('data menu href: %s', data_menu_url)
		return data_menu_url
