#Get All the links from the new releases page.
import scrapy
import psycopg2

def getrevieweridfromurl(url):
    return url.split("/member-reviews/")[1]

class ReviewerSpider(scrapy.Spider):
    name = "reviewers"
    allowed_domains = ["amazon.com"]
    conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
    cur = conn.cursor()
    cur.execute("""SELECT reviewerurl FROM reviewers""")
    temp = []
    rows = cur.fetchall()
    for row in rows:
        temp.append("http://www.amazon.com/gp/cdp/member-reviews/" + row[0].split("/profile/")[1])
        cur.execute("""UPDATE reviewers SET reviewerid = %s  WHERE reviewerurl = %s;""",(row[0].split("/profile/")[1].strip(),row[0]))
        conn.commit()
    start_urls = temp
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
        try :
            numberdiv = "".join(response.xpath("//b[contains(.,'Customer')]/../text()").extract()).encode("utf-8")
        except:
            pass
        reviewsnumber = int(filter(str.isdigit, numberdiv))
        reviewerid = getrevieweridfromurl(response.url)
        print topranking," ",helpfulvotes," ",reviewsnumber," ", response.url
        #conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
        #cur = conn.cursor()
        #SQL = "UPDATE reviewers SET topranking = %s, helpfulvotes = %s, reviewsnumber = %s, reviewerid = %s  WHERE revi"