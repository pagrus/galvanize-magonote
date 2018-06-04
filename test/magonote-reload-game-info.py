import psycopg2
import time
import os
import magonote_functions as mf

""" 

loads game info from html pages into the db, pretty much like magonote-get-game-info
but does not re-download html

"""
db_name = 'itchbot'
db_user = 'itchbot'
db_pw = 'IB!0502'
db_host = '127.0.0.1'

db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )

html_dir = 'html/latest'

html_file_list = [x for x in os.listdir(html_dir) if x[-5:] == ".html"]
for html_file in html_file_list:   
    file_path = "{}/{}".format(html_dir, html_file)
    game_list = mf.game_list_from_file(file_path)
    mf.insert_game_into_db(game_list, db_connection)
    
db_connection.close()
    
