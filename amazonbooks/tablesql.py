import psycopg2
conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
cur = conn.cursor()
cur.execute("""CREATE TABLE reviewers (
id SERIAL PRIMARY KEY,
date text NOT NULL,
amazonid text NOT NULL,
reviewer text,
reviewerurl text,
reviewerid text,
vinevoice boolean,
top10 boolean,
top50 boolean,
top100 boolean,
top500 boolean,
top1000 boolean,
halloffame boolean,
topranking int,
helpfulvotes int,
reviewsnumber int,
scrapedate DATE
);""")
conn.commit()