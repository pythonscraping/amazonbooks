#Get All the links from the new releases page.
import scrapy


def getasinfromurl(url):
    return url.split("/dp/")[1]

class ReviewerSpider(scrapy.Spider):
    name = "reviewers"
    allowed_domains = ["amazon.com"]
    start_urls = [
        "http://www.amazon.com/gp/cdp/member-reviews/ASCLLG44AITZW/",
        "http://www.amazon.com/gp/cdp/member-reviews/A1TUL3FFHYEXBK/"
    ]
    def parse(self, response):
        #item = HotRelease()
        div = response.xpath("//div[contains(@class,'tiny') and contains(.,'Top')]//text()")
        ranking = "".join(div.extract()).encode("utf-8")
        try :
            topranking = int(filter(str.isdigit, ranking.split('Helpful')[0]))
            helpfulvotes = int(filter(str.isdigit, ranking.split('Helpful')[1]))
        except:
            pass
        #number of reviews
        numberdiv = "".join(response.xpath("//b[contains(.,'Customer')]/../text()").extract()).encode("utf-8")
        reviewsnumber = int(filter(str.isdigit, numberdiv))
        print topranking," ",helpfulvotes," ",reviewsnumber