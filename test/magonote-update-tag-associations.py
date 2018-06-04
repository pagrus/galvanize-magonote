import psycopg2
import requests
import time
import magonote_functions as mf
from db_info import db_name, db_user, db_pw, db_host

"""

updates tag associations for a tag

at the time of writing the tags with low counts are 919, 928, 778

low 30s: 826, 906, 942, 914

"""

tag_list = list()

db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )

cur = db_connection.cursor()
cur.execute('SELECT tag_id FROM itch_tag_count_detail ORDER BY COUNT ASC')
all_itcd = cur.fetchall()

slice_itcd = all_itcd[150:200]

for tid in slice_itcd:
    tag_list.append(tid[0])
cur.close()

# list of tags
# tag_list = [919, 928, 778]

cur = db_connection.cursor()
for tag_id in tag_list:
    cur.execute('SELECT count, slug FROM itch_tag_count_detail WHERE tag_id=%s', (tag_id, ))
    tag_count = cur.fetchone()
    page_count = (tag_count[0] // 30) + 1
    print("count for tagid {} ({}): {}, {} pages".format(tag_id ,tag_count[1], tag_count[0], page_count))
    for tag_page in range(page_count):
        print("sleeping...")        
        time.sleep(2)
        game_list = mf.get_game_list_from_single_tag_page(tag_count[1], (tag_page + 1))
        print(game_list)
        mf.update_tag_associations(game_list, tag_id, db_connection)
cur.close()
db_connection.close()
