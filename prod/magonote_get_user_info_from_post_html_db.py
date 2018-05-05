import os
import psycopg2
from bs4 import BeautifulSoup as bs
import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

"""

looks through post html files for user urls, puts them in a set
these html files are stored in the db, other ones might be in the fs

helpful queries:
SELECT post_id, SUBSTRING (post_html, 195, 150) FROM itch_post_html LIMIT 10;

"""

user_urls = set()

db_connection=psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()

cur.execute("SELECT post_html FROM itch_post_html LIMIT 100")

for row in cur:
    html = row[0]
    soup = bs(html, "lxml")
    pa_span = soup.find_all("span", class_='post_author')
    if len(pa_span) > 0:
        pa_block = str(pa_span[0])
        print(pa_block[43:])
    cp_div = soup.find_all("div", class_='community_post')
    if len(cp_div) > 0:
        uid_block = str(cp_div[0])
        print(uid_block[70:100])

cur.close()
db_connection.close()