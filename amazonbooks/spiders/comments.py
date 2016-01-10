#Get all the comments information from a particular book.
import scrapy
from amazonbooks.items import Review


class ReleaseSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["amazon.com"]
    start_urls = [
        #Beware this one has 721 pages...
        "http://www.amazon.com/product-reviews/1607747308/ref=cm_cr_pr_btm_link_1?pageNumber=1"
    ]  

    def parse(self, response):
        item = Review()
        pagecount = int(response.url.split("pageNumber=")[1])
        #for comments in response.xpath(".//*[@id='cm_cr-review_list']//div") :
        for reviewcount,comments in enumerate(response.xpath(".//span[contains(@class,'review-text')]")) :
            reviewdiv = comments.xpath(".//../..")
            item['review'] = ''.join(comments.xpath(".//text()").extract()).encode("utf8")
            try:
                item['date'] = reviewdiv.xpath(".//span[contains(@class,'review-date')]/text()").extract()[0].encode("utf8")
            except IndexError:
                pass
            try:
                item['reviewer'] = reviewdiv.xpath(".//a[contains(@class,'author')]/text()").extract()[0].encode("utf8")
                item['reviewerurl'] = reviewdiv.xpath("./a[contains(@class,'author')]/@href").extract()[0].encode("utf8")
            except IndexError:
                pass

            #Compute the rating of the book by the presence of the css clas "a-star-rating"
            head = reviewdiv.xpath(".//i[contains(@class,'a-star-')]/@class").extract()[0].encode("utf8")
            if "a-star-5" in head:
                grade = 5
            elif "a-star-4" in head :
                grade = 4
            elif "a-star-3" in head  :
                grade = 3
            elif "a-star-2" in head :
                grade = 2
            elif "a-star-1" in head :
                grade = 1
            else :
                grade = "error"

            item['rating'] = grade
            item ['indexcount'] = pagecount * reviewcount
            item['id'] = reviewdiv.xpath("./@id").extract()[0].encode("utf8")


            #Format
            try:
                format = reviewdiv.xpath(".//a[contains(.,'Format:')]/text()").extract()[0].encode("utf8")
                item['format'] = format.split("Format:")[1].strip()
            except IndexError:
                item['format'] = "error"

            #Hepfulness of review
            try :
                helpfulspan = reviewdiv.xpath(".//span[contains(.,'review helpful')]/text()").extract()[0].encode("utf8")
                helpful = helpfulspan.split("of")[0].strip()
                total = helpfulspan.split("of")[1].split("people")[0].strip()
                item['helpful'] = int(filter(str.isdigit,helpful))
                item['total'] = int(filter(str.isdigit,total))
            except IndexError:
                pass


            item['title'] = reviewdiv.xpath(".//a[contains(@class,'a-text-bold')]/text()").extract()[0].encode("utf8")
            #Is it a verified purchase ?
            if "Verified Purchase" in reviewdiv.extract()[0]:
                verified = 1
            else :
                verified = 0
            item ['verified'] = verified
            yield item
"""
        try :
            nextlink = "http://www.amazon.com" + response.xpath(".//li[contains(@class,'a-last')]/a/@href").extract()[0]
            print nextlink
            yield scrapy.Request(nextlink)
        except IndexError:
            print "We stop here"
"""