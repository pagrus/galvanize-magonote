
import os
import psycopg2
import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

"""
loads post html into postgres from html directory
does not do any error checking eg for 404s or "page down for maintenance" etc

also does not check for duplicates although the id column is set to primary key
so they should be unique

be sure to use encoding="ISO-8859-1" when using open() on post files

"""

html_dir = '../html/post_pages'

post_list = [x for x in os.listdir(html_dir) if x[-5:] == ".html"]

db_connection=psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()

for post in post_list:
    post_id = int(post[:-5])
    post_path = "{}/{}".format(html_dir, post)
    with open (post_path, 'r', encoding="ISO-8859-1") as pfh:
        pf_html = pfh.read()
    print("inserting post id {}...".format(post_id))
    ins_tup = (post_id, pf_html)
    cur.execute("INSERT INTO itch_post_html (post_id, post_html) VALUES (%s, %s)", ins_tup)
    db_connection.commit()

cur.close()
db_connection.close()