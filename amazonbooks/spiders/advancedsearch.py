#Get links from the 100 pages of the advanced search.
import scrapy
from amazonbooks.items import LastRelease

import re
import datetime
import codecs

now = datetime.datetime.now()
hs = codecs.open("hst.txt","a","utf-8")

class ReleaseSpider(scrapy.Spider):
    name = "search"
    allowed_domains = ["amazon.com"]
    temp = []
    for i in range (1,100):
        url = "http://www.amazon.com/s/ref=sr_pg_" + str(i) + "?rh=n%3A283155%2Cp_45%3A1%2Cp_46%3AAfter%2Cp_47%3A2016&page=" + str(i) + "&sort=relevanceexprank&unfiltered=1&ie=UTF8&qid=1452210229"
        temp.append(url)
    start_urls = temp


    def parse(self, response):


        item = LastRelease()
        a = response.xpath("//*[contains(@id,'result_')]")
        for b in a :
            url = b.xpath("./div/div/div/div[2]/div[1]/a/@href").extract()[0]
            item['crawlDate'] = str(now)
            item['rank'] = int(b.xpath("./@id").extract()[0].encode("utf-8"))
            item['releaseDate'] = b.xpath("./div/div/div/div[2]/div[1]/span[3]/text()").extract()
            item['url'] = url
            m = re.search('dp\/(.*)', str(url))
            item['ASIN'] = m.group(0)[3:]
            yield item