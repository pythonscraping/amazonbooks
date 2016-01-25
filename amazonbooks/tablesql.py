import psycopg2
conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
cur = conn.cursor()
cur.execute("""CREATE TABLE reviews (
id SERIAL PRIMARY KEY,
asin text REFERENCES safelist(asin),
review text NOT NULL,
title text NOT NULL,
date text NOT NULL,
amazonid text NOT NULL,
reviewer text,
reviewerurl text,
format text,
rating INT,
helpful INT,
total INT,
verified boolean,
vinevoice boolean,
top10 boolean,
top50 boolean,
top100 boolean,
top500 boolean,
top1000 boolean,
halloffame boolean,
indexcount INT,
scrapedate DATE
);""")
conn.commit()