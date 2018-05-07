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

cur.execute("SELECT post_id, post_html FROM itch_post_html")
# cur.execute("SELECT post_id, SUBSTRING (post_html, 188, 100) FROM itch_post_html LIMIT 50")

insert_list = list()

for row in cur:
    html = row[1]
    soup = bs(html, "lxml")
    trail_anchors = soup.find_all('a', class_='trail')
    if len(trail_anchors) > 0:
        link_type = str(trail_anchors[0])[22:31]
        if link_type == '"https://':
            # print(link_type)
            # print(trail_anchors[0])
            link_str = str(trail_anchors[0])[31:-4]
            link_list = link_str.split('">')
            print(link_list)
        
            author_spans = soup.find_all('span', class_='post_author')
            if len(author_spans) > 0:
                author_str = str(author_spans[0])[44:-11]
                # print(author)
                author_list = author_str.split('">')
                print(author_list)
                # print(author_spans[0])
                # print("----------------------------------------\n\n")
    
                post_body = soup.find_all('div', class_='post_body')
                if len(post_body) > 0:
                    body_div = str(post_body[0])
                    print(len(body_div))
                    print("----------------------------------------\n\n")
                    
                    post_tup = (row[0], author_list[0], author_list[1], link_list[0], link_list[1], body_div)
                    insert_list.append(post_tup)
                    
for insert_tup in insert_list:
    print("inserting post {} div details...".format(row[0]))
    cur.execute("INSERT INTO itch_post_div_detail (post_id, user_slug, user_name, game_url, game_name, body_div) VALUES (%s, %s, %s, %s, %s, %s)", insert_tup)
    db_connection.commit()