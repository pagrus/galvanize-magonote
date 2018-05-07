#!/usr/bin/env python3

import os
import psycopg2
import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

"""

pull out comment scores, make a table to give to itemitem rec

postgres to dataframe solution from here
https://stackoverflow.com/questions/17156084/unpacking-a-sql-select-into-a-pandas-dataframe

"""
db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()

cur.execute('SELECT game_id, name, url FROM itch_game_detail_with_html WHERE game_html IS NULL ORDER BY RANDOM()')

# import psycopg2
# conn = psycopg2.connect("dbname='db' user='user' host='host' password='pass'")
# cur = conn.cursor()
# cur.execute("select instrument, price, date from my_prices")
df = DataFrame(cur.fetchall(), columns=['instrument', 'price', 'date'])
# then set index like

# df.set_index('date', drop=False)

# or directly:

# df.index =  df['date']

