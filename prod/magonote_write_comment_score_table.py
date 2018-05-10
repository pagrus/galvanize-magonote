#!/usr/bin/env python3

import os
import psycopg2
import pandas as pd
import numpy as np
import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

"""

pull out comment scores, write a tsv file

"""
db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()

# get userids, put in dict
# key is slug, val is userid
# just you know, to make it inconvenient
user_dict = dict()
cur.execute("SELECT user_id, slug FROM itch_user")
for user_row in cur:
    user_dict[user_row[1]] = user_row[0]


test_query = """
    SELECT user_slug, game_id, SUM(div_len) AS score 
    FROM itch_post_div_lengths 
    GROUP BY user_slug, game_id 
    ORDER BY RANDOM() 
    LIMIT 5000
"""

query = """
    SELECT user_slug, game_id, SUM(div_len) AS score 
    FROM itch_post_div_lengths 
    GROUP BY user_slug, game_id 
"""

file_list = list()
cur.execute(query)
for post_row in cur:
    if post_row[0] in user_dict:
        user_id = user_dict[post_row[0]]
        game_id = post_row[1]
        rating = post_row[2]
        stamp = 123456
        file_row = "{}  {}  {}  {}\n".format(user_id, game_id, rating, stamp)
        file_list.append(file_row)
    
with open ('test_post_data.idf', 'w') as fh:
    for file_line in file_list:    
        fh.write(file_line)