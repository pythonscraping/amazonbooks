# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import psycopg2


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
            SQL = "INSERT INTO books (url,asin,kindle,hardcover,paperback) VALUES (%s,%s,%s;%s;%s);"
            data = (item['url'], item['asin'],kindle,hardcover,paperback)
            cur.execute (SQL,data)
            conn.commit()
            #except:
            #    print "Database error"
            return item
        else:
            print item['url']

