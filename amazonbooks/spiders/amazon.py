#Get all the information about a book.
import scrapy
import re
import psycopg2

from amazonbooks.items import Book
from time import gmtime, strftime

def strToFloat(strFloat):
        """
        get a float number from a string, such as Price:$5.99
        :param strFloat:
        :return: float number
        """
        f = re.compile(r'\d+\.?\d*')
        try:
            result = float(f.search(strFloat).group())
        except AttributeError:
            result = 0
        return result

def getprice (type,value,book):
    if ("Kindle" in type) and value > 0:
        book['kindle'] = value
    if ("Hardcover" in type) and value > 0:
        book['hardcover'] = value
    if ("Paperback" in type) and not("Mass" in type) and value > 0:
        book['paperback'] = value
    if ("Mass Market Paperback" in type) and value > 0:
        book['massmarketpaperback'] = value

def getasinfromurl(url):
    return url.split("/dp/")[1].split("/")[0].split("?")[0]

class MyList(list):
    def utf(self):
        return [x.encode('utf-8') for x in self]

class AmazonSpider(scrapy.Spider):
    name = "amazons"
    allowed_domains = ["amazon.com"]
    conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
    cur = conn.cursor()
    cur.execute("""SELECT asin FROM safelist""")
    temp = []
    rows = cur.fetchall()
    for row in rows:
        temp.append("http://www.amazon.com/dp/" + row[0])
    start_urls = temp

    def parse(self, response):

        item = Book()
        if "not a robot" in response.body :
            print "detected " + response.url
            time.sleep(10)
            with open("detectedbooks.txt", "a") as myfile:
                myfile.write(response.url + "\n")
        item['url'] = response.url

        #Get asin from url
        item['asin'] = getasinfromurl(response.url)

        #Save file to html
        file_name = "bookpage:" + item['asin'] + " " + strftime("%Y-%m-%d %H:%M", gmtime())
        with open('files/%s.html' % file_name, 'w+b') as f:
            f.write(response.body)

        if "item has not been released" in response.body :
            item['ispreorder'] = "1"
        else :
            item['ispreorder'] = "0"
        # Description of the Book
        description = ''
        description = u''.join(response.xpath(".//*[@id='bookDescription_feature_div']/noscript/div/descendant::*/text()").extract())
        description += u''.join(response.xpath(".//*[@id='bookDescription_feature_div']/noscript/div/text()").extract())
        item['description'] = description.encode("utf-8")


        #Pages
        try:
            pages = response.xpath(".//table[contains(@id,'productDetailsTable')]//li[contains(.,'pages')]/text()").extract()[0].encode('utf-8')
            item ['pages'] = int(pages.split('pages')[0].strip())
        except IndexError:
            item ['pages'] = 'not found'



        #Allow Preview?
        if "sitbLogo" in response.body :
            item['allowpreview'] = "1"
        else :
            item['allowpreview'] = "1"

        #Extract listprice info
        try:
            listprice = response.xpath(".//span[@class='a-color-secondary a-text-strike']/text()").extract()[0]
            item['listprice'] = strToFloat(listprice)
        except IndexError:
            item['listprice'] = -1
        #Prices default values
        item['kindle'] = -1
        item['paperback'] = -1
        item['hardcover'] = -1
        item['massmarketpaperback'] = -1

        ### Extract the Price information using XPath ###
        for price in response.xpath(".//div[@id='twister']/div/span[@class='a-declarative']/table//tr") :
            try:
                priceType = price.xpath('./td[@class="dp-title-col"]/*[@class="title-text"]/span/text()').extract()[0].strip()
                priceValueString = price.xpath('./td[@class="a-text-right dp-price-col"]//span/text()').extract()[0].strip()
                priceValue = strToFloat(priceValueString)
                getprice(priceType,priceValue ,item)
            except IndexError:
                pass

        #General Information
        try:
            item['publisher'] = response.xpath(".//b[contains(text(),'Publisher')]/../text()").extract()[0].encode('utf-8').strip()
        except IndexError:
            item['publisher'] = 'null'

        try:
            item['isbn10'] = response.xpath(".//b[contains(text(),'ISBN-10')]/../text()").extract()[0].encode('utf-8').strip()
        except IndexError:
            item['isbn10'] = 'null'

        try:
            item['isbn13'] = response.xpath(".//b[contains(text(),'ISBN-13')]/../text()").extract()[0].encode('utf-8').strip()
        except IndexError:
            item['isbn13'] = 'null'

        try:
            item['dimensions'] = response.xpath(".//b[contains(text(),'Dimensions')]/../text()").extract()[0].encode('utf-8').strip()
        except IndexError:
            item['dimensions'] = 'null'

        #Average rating
        try:
            averagestr = response.xpath(".//span[contains(@class,'s_star_')]/@title").extract()[0].encode('utf-8').split("out")[0]
            item['average'] = strToFloat(averagestr)
        except IndexError:
            item['average'] = "-1"

        #Editorial review
        editorialh2 = response.xpath(".//h2[contains(text(),'Editorial Review')]/text()").extract()
        if (len(editorialh2) > 0):
            item['haseditorialreview'] = 1
        else:
            item['haseditorialreview'] = 0

        #Also bought (needs to cover additional cases)
        listoflinks1 = response.xpath(".//*[@id='purchase-sims-feature']//@href")
        listofasintemp = []
        listofasin = []
        for link in listoflinks1:
            if bool(re.search("/([0-9]{10})(?:[/?]|$)",link.extract().encode('utf-8'))):
                linktemp = re.search("/([0-9]{10})(?:[/?]|$)",link.extract().encode('utf-8')).group(0)
                listofasintemp.append(int(filter(str.isdigit,str(linktemp))))
            else:
                pass #it is false
        #Second case:
        listofasin = listofasin + list(set(listofasintemp))
        listoflinks2 = response.xpath(".//h2[contains(text(),'What Other Items')]/..//@href")
        listofasintemp = []
        for link in listoflinks2:
            if bool(re.search("/([0-9]{10})(?:[/?]|$)",link.extract().encode('utf-8'))):
                linktemp = re.search("/([0-9]{10})(?:[/?]|$)",link.extract().encode('utf-8')).group(0)
                listofasintemp.append(int(filter(str.isdigit,str(linktemp))))
            else:
                pass #it is false
        listofasin = listofasin + list(set(listofasintemp))
        item['alsobought'] = list(set(listofasin))



        #bestsellerrank
        bestsellerrankdirty = response.xpath(".//b[contains(text(),'Amazon Best')]/../text()").extract()
        try:
            bestsellerrankstring = "".join(bestsellerrankdirty).encode("utf-8")
            item['bestsellerrank'] = int(filter(str.isdigit, bestsellerrankstring)) # We get only the number information
        except:
            item['bestsellerrank'] = -1

        #Subranks
        rankdirty = response.xpath(".//li[contains(@class,'zg_hrsr_item')]")
        subranklist = []
        for rank in rankdirty :
            subrank = rank.xpath(".//span")
            subrankscore = int(filter(str.isdigit, subrank[0].extract().encode('utf-8')))
            subrankdetail = u''.join(MyList(subrank[1].xpath(".//descendant-or-self::*/text()").extract())).encode('utf-8').split("in")[1].strip()
            subranklist.append([subrankscore,subrankdetail])
        item['subrankdetail'] = subranklist

        yield item