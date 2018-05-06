
import os
from bs4 import BeautifulSoup as bs
import psycopg2
import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

"""

looks for user profile links in html pages, adds to db

"""
db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()

html_dir = "../html/post_pages"

html_file_list = [x for x in os.listdir(html_dir) if x[-5:] == ".html"]
partial_list = html_file_list[100:110]
list_length = len(html_file_list)
finc = 0

# hits the db for every html file, hmmmm
cur.execute('SELECT slug FROM itch_user')
slug_result = cur.fetchall()
slug_set =  set([item for sublist in slug_result for item in sublist])

for html_file in html_file_list:
    finc += 1
    html_path = html_dir + '/' + html_file
    print("processing {}, file {} of {}".format(html_path, finc, list_length))
    with open (html_path, 'r', encoding="ISO-8859-1") as fh:
        txt = fh.read()
    new_users = mf.get_userids_from_html(txt)

    if len(new_users) > 0:
        for new_slug in new_users:
            if new_slug not in slug_set:
                print("inserting new user {}".format(new_slug))
                cur.execute("INSERT INTO itch_user (slug) VALUES (%s)", (new_slug, ))
                db_connection.commit()
                slug_set.add(new_slug)