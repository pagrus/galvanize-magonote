import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import os
import pickle
import re
import random

# comments have already been downloaded (using curl)
# and are in html/post_pages/
# there are about 400,000 of them

# we want to get:
# game name
# game id if available
# post author name
# post author id
# post content
# post length
# timestamp
# anything else???

post_dir = 'html/post_pages'

post_list = [x for x in os.listdir(post_dir) if x[-5:] == ".html"]
# post_list.sort()
random.shuffle(post_list)
len(post_list)

pf_df = pd.DataFrame(columns=['user name', 'time stamp', 'span count', 'pee count', 'post div count', 'post div zero length', 'post div zero', 'trail anchor', 'link type', 'title'])

for file in post_list[:200]:
    # get post id from url
    pid_l = re.findall(r'\d+', file)
    pid = int(pid_l[0])
    
    # make a soup
    this_post = 'html/post_pages/' + file
    with open (this_post, 'r', encoding="ISO-8859-1") as fh:
        rt = fh.read()
    soup = bs(rt, "lxml")
    
    # get title
    title_txt = soup.title.string
    
    # get span count
    all_spans = soup.find_all('span')
    all_dates = soup.find_all('span', class_="post_date")
    all_authors = soup.find_all('span', class_="post_author")
    all_pees = soup.find_all('p')
    trail_anchor = soup.find_all('a', class_="trail")
    all_post_divs = soup.find_all('div', class_='post_content')
    post_div_count = len(all_post_divs)
    span_count = len(all_spans)
    pee_count = len(all_pees)
    
    if len(trail_anchor) > 0:
        trail_url = trail_anchor[0]['href']
        if trail_url[:8] == 'https://':
            anchor_type = 'https'
        else:
            anchor_type = 'relative'
    else:
        trail_url = '';
        anchor_type = '';
    
    if post_div_count > 0:
        post_div_zero = str(all_post_divs[0])
    else:
        post_div_zero = ''
        
    post_div_zero_length = len(post_div_zero)
    
    if span_count > 6:
        user_name = all_spans[1].string
        # stamp = all_spans[2]['title']
        stamp = all_dates[0]['title']
        
    else:
        user_name = ''
        stamp = ''
    
    pf_df.loc[pid] = [user_name, stamp, span_count, pee_count, post_div_count, post_div_zero_length, post_div_zero, trail_url, anchor_type,title_txt]
    