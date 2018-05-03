import psycopg2
import requests
import time
import magonote_functions as mf
# from db_info import db_name, db_user, db_pw, db_host

"""

reads list of tags from db, updates count from first tag listing page 

"""

db_name = 'itchbot'
db_user = 'itchbot'
db_pw = 'IB!0502'
db_host = '127.0.0.1'

db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )

# tag_id | slug | tag_desc 
cur = db_connection.cursor()
cur.execute('SELECT tag_id, slug FROM itch_tag')
tag_list = cur.fetchall()
for tag in tag_list:
    print("sleeping for 2s...")
    time.sleep(2)
    tag_url = "https://itch.io/games/newest/tag-{}".format(tag[1])
    r = requests.get(tag_url)
    rt = r.text
    game_count = mf.get_game_count_from_tag_html(rt)
    print("game count for {}: {}".format(tag[1], game_count))
    cur.execute("INSERT INTO itch_tag_count (tag_id, count) VALUES (%s, %s)", (tag[0], game_count))
    db_connection.commit()

cur.close()
db_connection.close()