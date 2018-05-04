
import os
import psycopg2
import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

"""
loads game html into postgres from data directory
assumes games are numbered by id
does not do any error checking eg for 404s or "page down for maintenance" etc

also does not check for duplicates although the id column is set to primary key
so they should be unique

might be better to load directly from website? hmmm

"""

html_dir = '../html/game_pages'

game_list = [x for x in os.listdir(html_dir) if x[-5:] == ".html"]

db_connection=psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()

for game in game_list:
    game_id = game[:-5]
    game_path = "{}/{}".format(html_dir, game)
    with open (game_path, 'r') as gfh:
        gf_html = gfh.read()
    print("inserting game id {}...".format(game_id))
    ins_tup = (game_id, gf_html)
    cur.execute("INSERT INTO itch_game_html (game_id, game_html) VALUES (%s, %s)", ins_tup)
    db_connection.commit()

cur.close()
db_connection.close()