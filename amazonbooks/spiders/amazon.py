#Get all the information about a book.
import scrapy
import re

from amazonbooks.items import Book

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



class AmazonSpider(scrapy.Spider):
    name = "amazons"
    allowed_domains = ["amazon.com"]
    start_urls = ["http://www.amazon.com/Firelight-Amulet-7-Kazu-Kibuishi/dp/0545433169",
                  "http://www.amazon.com/gp/product/0756607647/"]

    def parse(self, response):

        item = Book()

        item['url'] = response.url
        asinregex = re.search("/([a-zA-Z0-9]{10})(?:[/?]|$)",str(response.url)).group(0)
        item['asin'] = int(filter(str.isdigit,asinregex))


        # Description of the Book
        description = ''
        description = ''.join(response.xpath(".//*[@id='bookDescription_feature_div']/noscript/div/descendant::*/text()").extract())
        description += ''.join(response.xpath(".//*[@id='bookDescription_feature_div']/noscript/div/text()").extract())
        item['description'] = description.encode("utf-8")

        #Extract listprice info
        try:
            listprice = response.xpath(".//span[@class='a-color-secondary a-text-strike']/text()").extract()[0]
            item['listprice'] = strToFloat(listprice)
        except IndexError:
            item['listprice'] = 'null'

        ### Extract the Price information using XPath ###
        for price in response.xpath(".//div[@id='twister']/div/span[@class='a-declarative']/table/tr") :
            priceType = price.xpath('./td[@class="dp-title-col"]/*[@class="title-text"]/span/text()').extract()[0].strip()
            priceValue = strToFloat(price.xpath('./td[@class="a-text-right dp-price-col"]//span/text()').extract()[0].strip())
            getprice(priceType,priceValue ,item)
        try:
            item['publisher'] = str(response.xpath(".//b[contains(text(),'Publisher')]/../text()").extract()[0]).strip()
        except IndexError:
            item['publisher'] = 'null'

        try:
            item['isbn10'] = str(response.xpath(".//b[contains(text(),'ISBN-10')]/../text()").extract()[0]).strip()
        except IndexError:
            item['isbn10'] = 'null'

        try:
            item['isbn13'] = str(response.xpath(".//b[contains(text(),'ISBN-13')]/../text()").extract()[0]).strip()
        except IndexError:
            item['isbn13'] = 'null'

        try:
            item['dimensions'] = str(response.xpath(".//b[contains(text(),'Dimensions')]/../text()").extract()[0]).strip()
        except IndexError:
            item['dimensions'] = 'null'

        #Average rating
        try:
            averagestr = str(response.xpath(".//span[contains(@class,'s_star_')]/@title").extract()[0]).split("out")[0]
            item['average'] = strToFloat(averagestr)
        except IndexError:
            item['average'] = "no average"

        #bestsellerrank
        bestsellerrankdirty = response.xpath(".//b[contains(text(),'Amazon Best Sellers Rank')]/../text()").extract()
        bestsellerrankstring = str("".join(bestsellerrankdirty))
        item['bestsellerrank'] = int(filter(str.isdigit, bestsellerrankstring)) # We get only the number information
        #print "Result:", bestsellerrank
        yield item