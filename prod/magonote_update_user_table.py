
import os
from bs4 import BeautifulSoup as bs
import magonote_funcs as mf
from db_info import db_name, db_user, db_pw, db_host

"""

looks for user profile links in html pages, adds to db

"""

html_file = '../html/post_pages/270691.html'
with open (html_file, 'r') as fh:
    txt = fh.read()
new_users = mf.get_userids_from_html(txt)

print(new_users)