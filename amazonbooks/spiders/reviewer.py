#Get All the links from the new releases page.
import scrapy
import psycopg2
from time import gmtime, strftime

def getrevieweridfromurl(url):
    return url.split("/member-reviews/")[1].split("/")[0]

class ReviewerSpider(scrapy.Spider):
    name = "reviewers"
    allowed_domains = ["amazon.com"]
    conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
    cur = conn.cursor()
    cur.execute("""SELECT reviewerurl FROM reviewers WHERE scrapedate=%s""",('2016-02-04',))
    temp = []
    rows = cur.fetchall()
    for row in rows:
        temp.append("http://www.amazon.com/gp/cdp/member-reviews/" + row[0].split("/profile/")[1])
        cur.execute("""UPDATE reviewers SET reviewerid = %s  WHERE reviewerurl = %s;""",(row[0].split("/profile/")[1].split("/")[0].strip(),row[0]))
        conn.commit()
    start_urls = temp
    def parse(self, response):
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
        file_name = "reviewer:" + reviewerid + " " + strftime("%Y-%m-%d %H:%M", gmtime())
        with open('files/%s.html' % file_name, 'w+b') as f:
            f.write(response.body)
        print topranking," ",helpfulvotes," ",reviewsnumber," ", reviewerid
        #If top Ranking does not exist
        if 'topranking' in vars() :
            pass
        else:
            topranking = -1
        conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
        cur = conn.cursor()
        SQL = "UPDATE reviewers SET topranking = %s, helpfulvotes = %s, reviewsnumber = %s " \
              "WHERE reviewerid = %s AND scrapedate=%s"
        data = (topranking,helpfulvotes,reviewsnumber,reviewerid,'2016-02-04')
        cur.execute(SQL,data)
        conn.commit()