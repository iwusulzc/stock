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
			self.log('data menu url get failure', level=log.ERROR)
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
				self.log("stock name url missed", level=log.ERROR)
	 
			stock_code_pat = re.compile('\((.*)\)')

			for name, url in stock_list:
				stockListItem = StockListItem()

				stockListItem['exchange'] = sh
				stockListItem['name'] = name.split('(')[0]
				stockListItem['stock_code'] = stock_code_pat.findall(name)
				stockListItem['url'] = url

				yield stockListItem
			
	def parse_eastmoney_data_page(self, response):
		pass

	def data_menu_url_get(self, response):
		data_menu = response.xpath('//div[@class="nav"]/div[@class="navlist"]/ul[@class="mu101"]/li')[1]
		data_menu_url = data_menu.css('a::attr(href)')[3].extract()
		if data_menu_url:
			self.log('data menu href: ' + data_menu_url)
		return data_menu_url
