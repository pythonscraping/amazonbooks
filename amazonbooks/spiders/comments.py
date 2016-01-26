#Get all the comments information from a particular book.
import scrapy
from amazonbooks.items import Review
import psycopg2

def getasinfromurl(url):
    return url.split("/product-reviews/")[1].split("/")[0].split("?")[0]

class ReleaseSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["amazon.com"]
    #Connection to the database
    conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
    cur = conn.cursor()
    cur.execute("""SELECT asin FROM safelist""")
    temp = []
    rows = cur.fetchall()
    for row in rows:
        temp.append("http://www.amazon.com/product-reviews/" + row[0] + "/ref=cm_cr_pr_btm_link_1?pageNumber=1")
    start_urls = temp

    #start_urls = [
        #Beware this one has 721 pages...
        #"http://www.amazon.com/product-reviews/1607747308/ref=cm_cr_pr_btm_link_1?pageNumber=1",
        #"http://www.amazon.com/product-reviews/0544272994/ref=cm_cr_pr_btm_link_1?pageNumber=1"
    #]

    def parse(self, response):
        item = Review()
        pagecount = int(response.url.split("pageNumber=")[1])

        #Get asin from url
        #asinregex = re.search("/([a-zA-Z0-9]{10})(?:[/?]|$)",str(response.url)).group(0)
        #item['asin'] = str(filter(str.isdigit,asinregex))
        item['asin'] = getasinfromurl(str(response.url))
        mostcritical = response.xpath(".//h4[contains(.,'helpful critical')]/../../..//a[contains(@href,'customer-reviews')]/@href").extract()[0].encode("utf8")
        item['mostcritical'] = mostcritical
        #for comments in response.xpath(".//*[@id='cm_cr-review_list']//div") :
        for reviewcount,comments in enumerate(response.xpath(".//span[contains(@class,'review-text')]")) :
            reviewdiv = comments.xpath(".//../..") #main div containing a review
            item['review'] = ''.join(comments.xpath(".//text()").extract()).encode("utf8")
            try:
                item['date'] = reviewdiv.xpath(".//span[contains(@class,'review-date')]/text()").extract()[0].encode("utf8")
            except IndexError:
                pass
            try:
                item['reviewer'] = reviewdiv.xpath(".//a[contains(@class,'author')]/text()").extract()[0].encode("utf8")
                item['reviewerurl'] = reviewdiv.xpath(".//a[contains(@class,'author')]/@href").extract()[0].encode("utf8")
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
            item ['indexcount'] = (reviewcount + 1)+ (10 * (pagecount-1))
            item['id'] = reviewdiv.xpath("./@id").extract()[0].encode("utf8")


            #Format
            try:
                format = reviewdiv.xpath(".//a[contains(.,'Format:')]/text()").extract()[0].encode("utf8")
                item['format'] = format.split("Format:")[1].strip()
            except IndexError:
                item['format'] = "error"

            ####### TOP REVIEWERS ######
            #Vine Voice
            if "VINE VOICE" in reviewdiv.extract()[0]:
                item['vinevoice'] = 1
            else:
                item['vinevoice'] = 0

            if "TOP 10 REVIEWER" in reviewdiv.extract()[0]:
                item['top10Reviewer'] = 1
            else:
                item['top10Reviewer'] = 0

            if "TOP 50 REVIEWER" in reviewdiv.extract()[0]:
                item['top50Reviewer'] = 1
            else:
                item['top50Reviewer'] = 0

            if "TOP 100 REVIEWER" in reviewdiv.extract()[0]:
                item['top100Reviewer'] = 1
            else:
                item['top100Reviewer'] = 0

            if "TOP 500 REVIEWER" in reviewdiv.extract()[0]:
                item['top500Reviewer'] = 1
            else:
                item['top500Reviewer'] = 0

            if "TOP 1000 REVIEWER" in reviewdiv.extract()[0]:
                item['top1000Reviewer'] = 1
            else:
                item['top1000Reviewer'] = 0

            if "HALL OF FAME" in reviewdiv.extract()[0]:
                item['HallOfFameReviewer'] = 1
            else:
                item['HallOfFameReviewer'] = 0



            #Hepfulness of review
            try :
                helpfulspan = reviewdiv.xpath(".//span[contains(.,'review helpful')]/text()").extract()[0].encode("utf8")
                helpful = helpfulspan.split("of")[0].strip()
                total = helpfulspan.split("of")[1].split("people")[0].strip()
                item['helpful'] = int(filter(str.isdigit,helpful))
                item['total'] = int(filter(str.isdigit,total))
            except IndexError:
                item['helpful'] = 0
                item['total'] = 0
            if 'helpful' not in item :
                item['helpful'] = 0
            item['title'] = reviewdiv.xpath(".//a[contains(@class,'a-text-bold')]/text()").extract()[0].encode("utf8")
            #Is it a verified purchase ?
            if "Verified Purchase" in reviewdiv.extract()[0]:
                verified = 1
            else :
                verified = 0
            item ['verified'] = verified
            yield item

        try :
            nextlink = "http://www.amazon.com" + response.xpath(".//li[contains(@class,'a-last')]/a/@href").extract()[0]
            print nextlink
            yield scrapy.Request(nextlink)
        except IndexError:
            print "We stop here"
