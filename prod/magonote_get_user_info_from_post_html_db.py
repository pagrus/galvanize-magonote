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

cur.execute("SELECT post_html FROM itch_post_html LIMIT 500")

for row in cur:
    html = row[0]
    soup = bs(html, "lxml")
    cp_divs = soup.find_all("div", class_='community_post')
    ph_divs = soup.find_all("div", class_='post_header')
    if len(cp_divs) > 0:
        data_post = cp_divs[0]['data-post']  
        if len(data_post) > 0:
            user_id_split = data_post.split(',')
            user_id = user_id_split[0][11:]
            
    if len(ph_divs) > 0:
        ph_span = ph_divs[0].find_all('span')
        if len(ph_span[0]) > 0:
            user_name = ph_span[0].string
            try: 
                user_url = ph_span[0]('a')[0]['href'][9:]
            except:
                user_url = ''

cur.close()
db_connection.close()