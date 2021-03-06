# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import psycopg2
import datetime

class psqlpipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
        cur = conn.cursor()
        if (spider.name == "amazons") : #Only execute it for the amazons pipeline
            #print spider.name
            #try :
            kindle = float(item['kindle'])
            hardcover = float(item['hardcover'])
            paperback = float(item['paperback'])
            massmarketpaperback = float(item['massmarketpaperback'])
            listprice  = float(item['listprice'])
            publisher = item['publisher']
            isbn10 = item['isbn10']
            isbn13 = item['isbn13']
            average = float(item['average'])
            haseditorialreview = str(item['haseditorialreview'])
            allowpreview = str(item['haseditorialreview'])
            description = item['description']
            scrapedate = datetime.datetime.now()
            SQL = "INSERT INTO books (url,asin,kindle,hardcover,paperback,massmarketpaperback" \
                  ",listprice,publisher,isbn10,isbn13,average,haseditorialreview,allowpreview,description,scrapedate" \
                  ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            data = (item['url'], item['asin'],kindle,hardcover,paperback,massmarketpaperback
                    ,listprice,publisher,isbn10,isbn13,average,haseditorialreview,allowpreview,description,scrapedate)
            cur.execute (SQL,data)
            SQL2 = "INSERT INTO booksrank (asin,alsoboughtasin,bestsellerrank,scrapedate) VALUES (%s,%s,%s,%s);"
            data2 = (item['asin'],item['alsobought'],int(item['bestsellerrank']),scrapedate)
            cur.execute (SQL2,data2)
            for subrank in item['subrankdetail']:
                subrankscore = int(subrank[0])
                subrankdetail = subrank[1]
                SQL3 = "INSERT INTO booksrank (asin,subrank,subrankdetail,scrapedate) VALUES (%s,%s,%s,%s);"
                data3 = (item['asin'],subrankscore,subrankdetail,scrapedate)
                cur.execute (SQL3,data3)
            conn.commit()
            return item
        elif (spider.name == "releases"):
            SQL = "INSERT INTO safelist (asin,url,reason,releasedate,scrapedate) VALUES (%s,%s,%s,%s,%s);"
            data = (item['asin'], item['url'],"newreleases",item['releaseDate'],datetime.datetime.now())
            cur.execute (SQL,data)
            conn.commit()
        elif (spider.name == "search"):
            SQL = "INSERT INTO safelist (asin,url,reason,releasedate,rank,scrapedate) VALUES (%s,%s,%s,%s,%s,%s);"
            data = (item['ASIN'], item['url'],"february",item['releaseDate'],item['rank'],datetime.datetime.now())
            cur.execute (SQL,data)
            conn.commit()
        elif (spider.name == "reviews"):
            SQL = "INSERT INTO reviews (asin,review,title,date,amazonid,scrapedate" \
                  ",vinevoice, top10, top50,top100, top500, top1000, verified,indexcount," \
                  "helpful,total,rating,format,halloffame,reviewer,reviewerurl) " \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            data = (item['asin'],item['review'],item['title'],item['date'],item['id'],datetime.datetime.now()
                    ,str(item['vinevoice']),str(item['top10Reviewer']),str(item['top50Reviewer']),str(item['top100Reviewer']),
                    str(item['top500Reviewer']),str(item['top1000Reviewer']),str(item['verified']),
                    item['indexcount'],item['helpful'],item['total'],item['rating'],
                    item['format'], str(item['HallOfFameReviewer']),
                    item['reviewer'],item['reviewerurl'])
            cur.execute (SQL,data)
            #Insert mostcritical in booksrank if it does not exist already
            scrapedate = datetime.datetime.now()
            if (item["mostcritical"] != 'null' and len(item["mostcritical"]) > 5):
                SQL2 = "INSERT INTO booksrank (asin,mostcritical,scrapedate) SELECT %s,%s,%s WHERE NOT EXISTS (SELECT 1 FROM booksrank WHERE mostcritical = %s);"
                data2 = (item['asin'],item['mostcritical'],scrapedate, item['mostcritical'])
                cur.execute (SQL2,data2)
            #non existence of most helpful critical review:
            if (item["mostcritical"] == 'null'):
                SQL2 = "INSERT INTO booksrank (asin,mostcritical,scrapedate) SELECT %s,%s,%s WHERE NOT EXISTS (SELECT 1 FROM booksrank WHERE asin = %s);"
                data2 = (item['asin'],item['mostcritical'],scrapedate,item['asin'])
                cur.execute (SQL2,data2)
            conn.commit()
            #return item

        else:
            return item