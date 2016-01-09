import scrapy
from amazonbooks.items import HotRelease


class ReleaseSpider(scrapy.Spider):
    name = "releases"
    allowed_domains = ["amazon.com"]
    start_urls = [
        "http://www.amazon.com/gp/new-releases/books/ref=zg_bsnr_books_pg_1?ie=UTF8&pg=1",
        "http://www.amazon.com/gp/new-releases/books/ref=zg_bsnr_books_pg_2?ie=UTF8&pg=2",
        "http://www.amazon.com/gp/new-releases/books/ref=zg_bsnr_books_pg_3?ie=UTF8&pg=3",
        "http://www.amazon.com/gp/new-releases/books/ref=zg_bsnr_books_pg_4?ie=UTF8&pg=4"
    ]
    def parse(self, response):
		item = HotRelease()
		for link in response.xpath(".//*[@id='zg_centerListWrapper']//div/div[2]/div[2]/a/@href"):
			item['url'] = link.extract().strip()
			for date in response.xpath(".//*[@id='zg_centerListWrapper']//div/div[2]/div[5]/text()"):
				item['releaseDate'] = date.extract().strip()
				yield item
		#pass