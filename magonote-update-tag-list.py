import psycopg2
import requests
import magonote_functions as mf
from db_info import db_name, db_user, db_pw, db_host

"""

gets the freshest tag list, updates tag table to reflect any additions
not sure if tags ever get deleted but this does not check for them

"""

tag_list_url = 'https://itch.io/tags'

r = requests.get(tag_list_url)
rt = r.text
tag_info = mf.get_tag_info(rt)

db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )

# tag_id | slug | tag_desc 
cur = db_connection.cursor()
cur.execute('SELECT slug FROM itch_tag')
ts_result = cur.fetchall()
tag_slug_set =  set([item for sublist in ts_result for item in sublist])
for tag in tag_info:
    if tag[0] not in tag_slug_set:
        cur.execute("INSERT INTO itch_tag (slug, tag_desc) VALUES (%s, %s)", (tag[0], tag[1]))
        db_connection.commit()

cur.close()
db_connection.close()

