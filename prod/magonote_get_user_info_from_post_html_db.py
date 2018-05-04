import os
import psycopg2
import re
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

cur.execute("SELECT post_html FROM itch_post_html LIMIT 10")

pattern = re.compile(r'/profile/.+class="avatar_container">')

for row in cur:
    html = row[0]
    pro_match = pattern.findall(html)
    if len(pro_match) != 0:
        pro_url = pro_match[0].split('"')[0]
        user_urls.add(pro_url[9:])
        
print(user_urls)



cur.close()
db_connection.close()