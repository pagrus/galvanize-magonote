import os
import magonote_functions as mf
import random
import pandas as pd
import numpy as np

# copied right out of the jupyter notebook to start

# ok we're assuming we have all the post data fetched already, and it's in html/post_pages

post_page_dir = "html/post_pages"

post_list = [x for x in os.listdir(post_page_dir) if x[-5:] == ".html"]
random.shuffle(post_list)
single_post = post_list[13]

len(post_list)

# ok looks good so far

partial_post_list = post_list[:1000]

temp_list = mf.get_post_info(partial_post_list, post_page_dir)

cols = ['trail anchor count', 'trail anchor zero', 'post div count','d0 length','d0 spans', 'user span', 'date span']
post_info_df = pd.DataFrame(columns=cols)

for item in temp_list:
    pid = item[0]
    post_info_df.loc[pid] = [item[1],item[2],item[3],item[4],item[5],item[6],item[7]]
    
pickle_name = 'comments_data.pkl'
csv_name = 'data/post_info.csv'

#pf_df.to_pickle(pickle_name)
post_info_df.to_csv(csv_name, sep='\t', encoding='utf-8')

# a 10000 line csv is 9.1MB