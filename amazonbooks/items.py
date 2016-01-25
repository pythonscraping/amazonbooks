# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
#List of our objects fields

import scrapy

class Book(scrapy.Item):
    url = scrapy.Field()
    kindle 	   = scrapy.Field(default = -1)
    hardcover  = scrapy.Field(default = -1)
    paperback  = scrapy.Field(default =-1)
    massmarketpaperback = scrapy.Field(default=-1)
    description = scrapy.Field()
    listprice = scrapy.Field()
    publisher = scrapy.Field()
    isbn10 = scrapy.Field()
    isbn13 = scrapy.Field()
    dimensions = scrapy.Field()
    bestsellerrank = scrapy.Field()
    #Subranks
    average = scrapy.Field()
    asin = scrapy.Field()
    haseditorialreview = scrapy.Field()
    alsobought = scrapy.Field()
    ispreorder = scrapy.Field()
    pages = scrapy.Field()
    allowpreview = scrapy.Field()
    subrankscore = scrapy.Field()
    subrankdetail = scrapy.Field()

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

class Review(scrapy.Item):
    review = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    #author = scrapy.Field()
    #authorLink = scrapy.Field()
    rating = scrapy.Field()
    verified = scrapy.Field()
    reviewer = scrapy.Field()
    reviewerurl = scrapy.Field()
    id = scrapy.Field()
    indexcount = scrapy.Field() #the lowest the highest the comment.
    helpful = scrapy.Field()
    total = scrapy.Field()
    format = scrapy.Field() #Binding
    #TOP reviewers
    vinevoice = scrapy.Field() #Trusted by Amazon
    top10Reviewer = scrapy.Field()
    top50Reviewer = scrapy.Field()
    top100Reviewer = scrapy.Field()
    top500Reviewer = scrapy.Field()
    top1000Reviewer	= scrapy.Field()
    HallOfFameReviewer = scrapy.Field()