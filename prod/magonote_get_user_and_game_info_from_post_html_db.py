from bs4 import BeautifulSoup as bs
import psycopg2
import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

"""

determine if a post comment refers to a game. if it does, get the game id, user and comment length
also set comment type to game or something

game urls take the form https://game_creator.itch.io/game_name

pb - title starts with "post by"
io - title is itch.io (always 404?)
ei - everything else
totals: pb = 330795, io = 69303, ei = 0


"""

db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()

# cur.execute("SELECT post_html FROM itch_post_html LIMIT 100")
cur.execute("SELECT post_id, SUBSTRING (post_html, 188, 14) FROM itch_post_html")

pb = 0
io = 0
ei = 0

for row in cur:
    print(row[1])
    if row[1] == "<title>Post by":
        pb += 1
    elif row[1] == "<title>itch.io":
        io += 1
    else:
        ei += 1

print("totals: pb = {}, io = {}, ei = {}".format(pb, io, ei))