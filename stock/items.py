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
