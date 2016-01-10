# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
#List of our objects fields

import scrapy

class Book(scrapy.Item):
    url = scrapy.Field()
    kindle 	   = scrapy.Field()
    hardcover  = scrapy.Field()
    paperback  = scrapy.Field()
    massmarketpaperback = scrapy.Field()
    description = scrapy.Field()
    listprice = scrapy.Field()
    publisher = scrapy.Field()
    isbn10 = scrapy.Field()
    isbn13 = scrapy.Field()
    dimensions = scrapy.Field()
    bestsellerrank = scrapy.Field()
    average = scrapy.Field()
    asin = scrapy.Field()
    haseditorialreview = scrapy.Field()
    alsobought = scrapy.Field()
    ispreorder = scrapy.Field()

class HotRelease(scrapy.Item):
    url = scrapy.Field()
    releaseDate = scrapy.Field()
    rank = scrapy.Field()
    asin = scrapy.Field()


class LastRelease(scrapy.Item):
    url = scrapy.Field()
    releaseDate = scrapy.Field()
    ASIN = scrapy.Field()
    rank = scrapy.Field()
    crawlDate = scrapy.Field()