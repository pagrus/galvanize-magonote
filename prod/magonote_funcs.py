
import requests
import os
import time

from bs4 import BeautifulSoup as bs

def get_userids_from_html(html_txt):
    """

    looks for user profile links in html pages, returns set

    """
    user_slug = set()
    rel_pre = '/profile/'
    rpl = len(rel_pre)
    abs_pre = 'https://itch.io/profile/'
    apl = len(abs_pre)
    soup = bs(html_txt, "lxml")
    
    all_links = soup.find_all('a', href=True)
    if len(all_links) > 0:
        for link in all_links:
            href = link['href']
            # print(href)
            if href[:apl] == abs_pre:
                user_slug.add(href[apl:])
            if href[:rpl] == rel_pre:
                user_slug.add(href[rpl:])    
    return user_slug
