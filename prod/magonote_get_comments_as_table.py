#!/usr/bin/env python3

import os
import psycopg2
import pandas as pd
import numpy as np
import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

"""

pull out comment scores, make a table to give to itemitem rec

postgres to dataframe solution from here
https://stackoverflow.com/questions/17156084/unpacking-a-sql-select-into-a-pandas-dataframe

"""
db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()

query = """
    SELECT user_slug, game_url, SUM(div_len) AS score 
    FROM itch_post_div_lengths 
    GROUP BY user_slug, game_url 
    ORDER BY RANDOM() 
    LIMIT 25
"""

# cur.execute('SELECT user_slug, game_url, SUM(div_len) AS score FROM itch_post_div_lengths GROUP BY user_slug, game_url ORDER BY RANDOM() LIMIT 25')
cur.execute(query)

# import psycopg2
# conn = psycopg2.connect("dbname='db' user='user' host='host' password='pass'")
# cur = conn.cursor()
# cur.execute("select instrument, price, date from my_prices")
df = pd.DataFrame(cur.fetchall(), columns=['user slug', 'game url', 'score'])
# then set index like

# df.set_index('date', drop=False)

# or directly:

# df.index =  df['date']

print(df)