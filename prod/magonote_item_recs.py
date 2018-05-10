import numpy as np
import pandas as pd
import psycopg2
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from time import time

import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

db_connection = psycopg2.connect( database=db_name, user=db_user, host=db_host, password=db_pw )
cur = db_connection.cursor()   

cur.execute('SELECT DISTINCT user_id FROM itch_post_div_full_lengths_subset')
uid_list = sorted([u[0] for u in cur])
cur.execute('SELECT DISTINCT game_id FROM itch_post_div_full_lengths_subset')
gid_list = sorted([g[0] for g in cur])
# print(uid_list, gid_list)

user_count = len(uid_list)
game_count = len(gid_list)
neighborhood_size = 75

query = """
    SELECT user_id, game_id, div_len, utime 
    FROM itch_post_div_full_lengths_subset; 
"""

cur.execute(query)

scores_matrix = sparse.lil_matrix((user_count, game_count))
for row in cur:
            # subtract 1 from id's due to match 0 indexing
    scores_matrix[uid_list.index(row[0]), gid_list.index(row[1])] = row[2]
    # print(row)

# print(scores_matrix)

item_sim_mat = cosine_similarity(scores_matrix.T)

least_to_most_sim_indexes = np.argsort(item_sim_mat, 1)
neighborhoods = least_to_most_sim_indexes[:, -neighborhood_size:]

# print(neighborhoods)

def pred_one_user(user_id):
    this_uid_index = uid_list.index(user_id)

    items_rated_by_this_user = scores_matrix[this_uid_index].nonzero()[1]
    one_user_pred = np.zeros(game_count)
    for item_to_rate in range(game_count):
        relevant_items = np.intersect1d(neighborhoods[item_to_rate],
                                        items_rated_by_this_user,
                                        assume_unique=True)  
        one_user_pred[item_to_rate] = scores_matrix[this_uid_index, relevant_items] * \
               item_sim_mat[item_to_rate, relevant_items] / \
               item_sim_mat[item_to_rate, relevant_items].sum()

    ret_pred = np.nan_to_num(one_user_pred)
    return ret_pred

tuid = 1342
tuser_pred = pred_one_user(tuid)
print(tuser_pred)

def pred_all_users():
    all_ratings = [pred_one_user(uid_list[user_id]) for user_id in range(user_count)]
    return np.array(all_ratings)

print(pred_all_users())

