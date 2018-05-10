#!/usr/bin/env python3

import os
import time
import requests
from bs4 import BeautifulSoup as bs
import psycopg2
import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

"""

looks for games that have comment pages, returns list?

actually it doesn't do thst. this looks for records in the it_game table that do not have html in the itch_game_html
table and attempts to fill those in

will be useful if all you have is a game id and url, like from the game browse pages for example

"""
db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()

cur.execute('SELECT game_id, name, url FROM itch_game_detail_with_html WHERE game_html IS NULL ORDER BY RANDOM()')
null_game_result = cur.fetchall()
nglen = len(null_game_result)

print("found {} game rows with null html fields".format(nglen))

nullcount = 0

for null_game in null_game_result:
    nullcount += 1
    print("sleeping 2s...")
    time.sleep(1)
    
    game_url = null_game[2]
    nullpct = (nullcount * 100) // nglen
    print("attempting to retrieve {} - item {} of {} - {}% of total".format(game_url, nullcount, nglen, nullpct))
    r = requests.get(game_url)
    if r.status_code == 200:
        game_html = r.text
        # print(game_html)
        game_id = null_game[0]
        game_tup = (game_id, game_html)
        print("inserting html for game {}...".format(game_id))
        cur.execute("INSERT INTO itch_game_html (game_id, game_html) VALUES (%s, %s)", game_tup)
        db_connection.commit()
        
cur.close()
db_connection.close()