import os
import random
import psycopg2
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction import text

from db_info import db_name, db_user, db_pw, db_host

"""

get html from postgres, chuck into kmeans


"""
db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()

query = """
    SELECT game_id, name, url, game_html 
    FROM itch_game_detail_with_html 
    WHERE game_html IS NOT NULL
    LIMIT 100;
"""

cur.execute(query)
game_df = pd.DataFrame(cur.fetchall(), columns=['game id', 'game name', 'game url', 'html'])
print(game_df)

# yeah uh you're going to have to beautifulsoup the html at some point

add_stop_words = ('commentslog', 'loader_outer', 'loading_lightbox', 
    'itchio', 'report', 'zip', 'view', 'comment', 'post', 'upvotes', 
    'account', 'post_id', 'report_url', 'io', 'game', 'nowname', 
    'priceclick', 'download', 'mb', 'downloadable', 'viewgame', 
    'user_tools', 'https', 'viewhtmlgame', 'start_maximized', 'htmlembed', 
    'play_after', 'itch', '_merchantsettings', 'document', 'apple', 
    'itunes', 'itunes_autolinkmaker', 'script', 'src', 'javascript', 
    'function', 'http', 'swf', 'flash', 'class', 'data', 'googleaccessid', 
    'gserviceaccount', 'signature', 'moonscript2', 'commondatastorage', 
    'div', 'js', 'span', 'default', 'var', 'usd', 'up_score', 
    'down_score', 'autolinkmaker', 'com', 'autolink','commentlog', 
    'html', 'play_url')
all_stop_words = text.ENGLISH_STOP_WORDS.union(add_stop_words)
itch_stop_words=set(all_stop_words)

vectorizer = TfidfVectorizer(stop_words=itch_stop_words)
X = vectorizer.fit_transform(game_df['html'])
features = vectorizer.get_feature_names()
num_clusters = 12
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(X)

top_centroids = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
for num, centroid in enumerate(top_centroids):
    print("%d: %s" % (num, ", ".join(features[i] for i in centroid)))