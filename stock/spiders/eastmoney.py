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
		js = string.format("document.querySelectorAll('#ZYZBTab li')[%d].click()", args.period)
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

	"""
	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url, self.parse, args={'wait': 10})
	"""

	def start_requests(self):
		url = "http://emweb.securities.eastmoney.com/f10_v2/OperationsRequired.aspx?type=web&code=sz000002"
		yield SplashRequest(url, self.transfer_page, args={'wait': 10})

	def parse(self, response):
		#stockListLoader = ItemLoader(item = StockListItem, response = response)

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
				_name = name.split('(')[0]
				code = stock_code_pat.findall(name)

				self.logger.info("parse %s, %s", _name, code)

				yield SplashRequest(url, callback = self.parse_stock_page, args={'wait': 20})
                                
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
                companySurvey_url = response.xpath('//li[@id="CompanySurvey"]/a/@href').extract()[0]
                if companySurvey_url:
                        yield SplashRequest(response.urljoin(companySurvey_url), callback = self.parse_company_survey_page, args={'wait': 20})
                        
        def parse_company_survey_page(self, response):
                stockItem = StockItem()

                trs = response.xpath('//table[@id="Table0"]/tbody/tr')

                tm = {u'A股代码' : 'code',
                      u'A股简称' : 'name',
                      u'上市交易所' : 'exchange',
                      u'所属证监会行业' : 'industry',
                      u'区域' : 'region',
                      u'注册资本(元)' : 'reg_capital',
                      u'公司简介' : 'company_profile',
                      u'经营范围' : 'scope_business',
                      }
                for tr in trs[3 :]:
                        ths = tr.xpath('th/text()').extract()
                        tds = tr.xpath('td/text()').extract()

                        for th, td in zip(ths, tds):
                                if th not in tm:
                                        continue
                                key = tm[th]
                                stockItem[key] = td
                # next page: 财务分析
                financial_analysis_url = response.xpath('//li[@id="NewFinanceAnalysis"]/a/@href').extract()[0]
                r = SplashRequest(response.urljoin(financial_analysis_url), callback = self.parse_financial_analysis_page, args={'wait': 20})
                r.meta['item'] = stockItem
                yield r        

        # 财务分析页面
	def parse_financial_analysis_page(self, response):
		tm = {
				u'基本每股收益(元)' : 'esp',
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

                stockItem = response.meta['item']
                stockItem['main_indicator'] = []
                
		# main indicator table
		trs = response.xpath('//div[@id="divzyzb"]/table/tbody/tr')

		#处理表头，取出报告期日期
		period = []
		ths = trs[0].xpath('th')

		for th in ths:
                        value = th.xpath('span/text()').extract()[0]
			period.append(value)

		if not period:
			pass

		tds_value = []

		for tr in trs:
			# 处理表的具体内容
			tds = tr.xpath('td')
			td_value = []

			for td in tds:
				value = td.xpath('span/text()').extract()[0]
				td_value.append(value)
			tds_value.append(td_value)

		for x in range(1, len(tds_value[0])):
			stockMainIndicator = StockMainIndicator()
			for y in range(1, len(tds_value)):
				key = tds_value[y][0]
				if key not in tm:
					break
				item = tm[key]
				stockMainIndicator[item] = tds_value[y][x]
			stockMainIndicator['period'] = period[x]
			stockItem['main_indicator'].append(stockMainIndicator)
		current = response.xpath('//ul[@id="zyzbTab"]/li[@class="current"]/text()').extract()[0]
                if current != u'按单季度':
                        # next page:
                        pass
                else:
                        
                        if current == u'按报告期':
                                page = 1
                        elif current == u'按年度':
                                page = 2
                        else:
                                page = 0

                        if page > 0:
                                SplashRequest(response.url, \
                                        callback = self.parse_financial_analysis_page, endpoint='execute', \
                                        args={'lua_source': script, 'wait': 10, 'period': page})
                                r.meta['item'] = stockItem
                                yield r
			
	def __parse_cpbd_page(self, response):
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

		stock_main_indicator_url = response.urljoin(response.xpath('//div[@id="zyzb"]/a/@href').extract()[0])

		for page in range(0, 3):
			yield SplashRequest(stock_main_indicator_url, \
				callback = self.parse_financial_analysis_page, endpoint='execute', \
				args={'lua_source': script, 'wait': 10, 'period': page})

	def data_menu_url_get(self, response):
		data_menu = response.xpath('//div[@class="nav"]/div[@class="navlist"]/ul[@class="mu101"]/li')[1]
		data_menu_url = data_menu.css('a::attr(href)')[3].extract()
		if data_menu_url:
			self.logger.debug('data menu href: %s', data_menu_url)
		return data_menu_url
