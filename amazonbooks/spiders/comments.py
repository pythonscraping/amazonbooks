#Get all the comments information from a particular book.
import scrapy
from amazonbooks.items import HotRelease


class ReleaseSpider(scrapy.Spider):
    name = "comments"
    allowed_domains = ["amazon.com"]
    start_urls = [
        "http://www.amazon.com/product-reviews/1607747308/ref=cm_cr_pr_btm_link_1?pageNumber=1"
    ]  

    def parse(self, response):
        for comments in response.xpath(".//*[@id='cm_cr-review_list']//div") :
            comment = comments.xpath("./div[5]/span[contains(@class,'review-text')]/text()").extract()
            date = comments.xpath("./div[3]/span[contains(@class,'review-date')]/text()").extract()
            author = comments.xpath("div[3]/span[1]/a[contains(@class,'author')]/text()").extract()
            authorLink = comments.xpath("div[3]/span[1]/a[contains(@class,'author')]/@href").extract()
            #Compute the rating of the book by the presence of the css clas "a-star-rating"
            if "a-star-5" in comments.extract() :
                grade = 5
            elif "a-star-4" in comments.extract():
                grade = 4
            elif "a-star-3" in comments.extract() :
                grade = 3
            elif "a-star-2" in comments.extract() :
                grade = 2
            elif "a-star-1" in comments.extract() :
                grade = 1
            else :
                grade = "error"

            #Is it a verified purchase ?
            if "Verified Purchase" in comments.extract() :
                verified = 1
            else :
                verified = 0

            if comment :
                print "-------------"
                print comment
                print date
                print author
                print authorLink
                print grade
                print verified

        #yield scrapy.Request('http://www.amazon.com/product-reviews/1250066115/ref=cm_cr_pr_btm_link_1?pageNumber=1')