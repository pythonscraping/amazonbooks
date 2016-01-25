#Get All the links from the new releases page.
import scrapy
from amazonbooks.items import HotRelease


def getasinfromurl(url):
    return url.split("/dp/")[1]

class ReleaseSpider(scrapy.Spider):
    name = "releases"
    allowed_domains = ["amazon.com"]
    start_urls = [
        "http://www.amazon.com/gp/new-releases/books/ref=zg_bsnr_books_pg_1?ie=UTF8&pg=1",
        "http://www.amazon.com/gp/new-releases/books/ref=zg_bsnr_books_pg_2?ie=UTF8&pg=2",
        "http://www.amazon.com/gp/new-releases/books/ref=zg_bsnr_books_pg_3?ie=UTF8&pg=3",
        "http://www.amazon.com/gp/new-releases/books/ref=zg_bsnr_books_pg_4?ie=UTF8&pg=4",
        "http://www.amazon.com/gp/new-releases/books/ref=zg_bsnr_books_pg_4?ie=UTF8&pg=5"
    ]
    def parse(self, response):
        item = HotRelease()
        for link in response.xpath(".//*[@id='zg_centerListWrapper']//div/div[2]/div[2]/a"):
            url = link.xpath("./@href").extract()[0].strip()
            item['url'] = str(url)
            item['asin'] = getasinfromurl(str(url))
            date = link.xpath("../../../div[2]/div[5]/text()")
            item['releaseDate'] = date.extract()[0].strip()
            yield item
        #pass