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
        if (spider.name == "amazons") : #Only execute it for the amazons pipeline
            #print spider.name
            #try :
            conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
            cur = conn.cursor()
            kindle = float(item['kindle'])
            hardcover = float(item['hardcover'])
            paperback = float(item['paperback'])
            SQL = "INSERT INTO books (url,asin,kindle,hardcover,paperback) VALUES (%s,%s,%s,%s,%s);"
            data = (item['url'], item['asin'],kindle,hardcover,paperback)
            cur.execute (SQL,data)
            conn.commit()
            #except:
            #    print "Database error"
            return item
        elif (spider.name == "releases"):
            conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
            cur = conn.cursor()
            SQL = "INSERT INTO safelist (asin,url,reason,releasedate,scrapedate) VALUES (%s,%s,%s,%s,%s);"
            data = (item['asin'], item['url'],"newreleases",item['releaseDate'],datetime.datetime.now())
            cur.execute (SQL,data)
            conn.commit()

        elif (spider.name == "reviews"):
            conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
            cur = conn.cursor()
            SQL = "INSERT INTO reviews (asin,review,title,date,amazonid,scrapedate) VALUES (%s,%s,%s,%s,%s;%s);"
            data = (item['asin'],item['review'],item['title'],item['date'],item['id'],datetime.datetime.now())
            cur.execute (SQL,data)
            conn.commit()
            return item

        else:
            return item