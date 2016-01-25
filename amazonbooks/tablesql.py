import psycopg2
conn = psycopg2.connect("dbname=amazon user=amazon password=amazon host=127.0.0.1")
cur = conn.cursor()
cur.execute("""CREATE TABLE safelist (
id SERIAL PRIMARY KEY,
asin text UNIQUE NOT NULL,
url text NOT NULL,
reason text NOT NULL,
releasedate text NOT NULL,
scrapedate DATE
);""")
cur.execute("""CREATE TABLE books(
id SERIAL PRIMARY KEY,
url text NOT NULL,
asin text UNIQUE NOT NULL,
kindle real,
hardcover real,
paperback real,
massmarketpaperback real,
listprice real,
publisher text,
isbn10 text,
isbn13 text,
dimensions text,
bestsellerrank INT,
average real,
haseditorialreview INT,
allowpreview INT,
scrapedate DATE
);""")
cur.execute(""" CREATE TABLE alsobought(
id SERIAL PRIMARY KEY,
asin text REFERENCES books(asin),
alsoboughtasin text NOT NULL
);""")
conn.commit()