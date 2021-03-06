import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import os
import pickle
import boto3
import re
import time

def get_game_count_from_tag_html(html):
    soup = bs(html, "lxml")
    count_class = "game_count"
    gcount = soup.find("nobr", class_=count_class)
    gctxt = gcount.get_text()
    gcdig = u''.join(c for c in gctxt if '0' <= c <= '9')
    # gctup = (tag[0], tag[1], gcdig, tag[2])
    return int(gcdig)

def get_latest_game_list(page):
    lurl = "https://itch.io:443/games/newest?page={}".format(page)
    lpath = "html/latest/{}.html".format(page)
    r = requests.get(lurl)
    if r.status_code == 200:
        with open(lpath, 'wb') as lfh:
            lfh.write(r.content)

def agg_tag_asses(tag_top):
    big_ass_list = list()
    for item in os.listdir(tag_top):
        tagdir = tag_top + '/' + item
        if os.path.isdir(tagdir):
            this_ass_set = mf.get_tag_assignments(tagdir)
            big_ass_list.append(this_ass_set)
    return big_ass_list

def get_tag_assignments(tag_dir):
    tag_assignments = list()    
    tag_file_list = [x for x in os.listdir(tag_dir) if x[-5:] == ".html"]
    for tag_html_file in tag_file_list:
        file_path = tag_dir + '/' + tag_html_file
        with open (file_path, 'r') as tfh:
            tf_html = tfh.read()
        soup = bs(tf_html, "lxml")
        title_divs = soup.find_all("div", class_='game_title')
        for game in title_divs:
            anchor = game.find('a')
            href = anchor['href']            
            ass_tup = (tag_dir[15:], href)
            tag_assignments.append(ass_tup)
    return tag_assignments

def get_tag_info(tag_html):
    soup = bs(tag_html, "lxml")
    div_class = "tag_list"
    tag_div = soup.find("div", class_=div_class)
    tag_anchors = tag_div.find_all("a")
    tag_list = list()
    for ta in tag_anchors:
        turl = ta['href']
        tlab = ta['data-label']
        ttxt = ta.get_text()
        ttup = (tlab, ttxt, turl)
        tag_list.append(ttup)
    return tag_list
    
def get_tag_html(tag_list):
    for tag in tag_list:
        # compare https://itch.io:443/games/newest/genre-action
        turl = "https://itch.io:443/games/newest/tag-" + tag[0]
        tpath = "html/tags/" + tag[0] + ".html"
        r = requests.get(turl)
        if r.status_code == 200:
            with open(tpath, 'wb') as tfh:
                tfh.write(r.content)
                
def parse_tag_html(tag_dir):
    tag_details = list()    
    tag_file_list = [x for x in os.listdir(tag_dir) if x[-5:] == ".html"]
    for tag_file in tag_file_list:
        tag_slug = tag_file[:-5]
        tag_path = tag_dir + tag_file
        with open (tag_path, 'r') as tffh:
            tft = tffh.read()
        tsoup = bs(tft, "lxml")
        fpg = tsoup.find_all("div", class_="game_cell_data")
        gcfp = len(fpg)
        gcnb = tsoup.find("nobr", class_="game_count")
        game_count_text = gcnb.get_text()
        game_count_str = re.findall('\d+', game_count_text)
        game_count = int(''.join(game_count_str))
        tag_tup = (tag_slug, game_count, gcfp)
        tag_details.append(tag_tup)
    return tag_details
    
def get_games_from_tag(tag_slug, game_count):
    html_base_path = 'html/tags'
    # https://itch.io/games/newest/tag-horror?page=2
    n_pages = ( game_count // 30 ) + 1
    tag_url_base = "https://itch.io/games/newest/tag-"
    for page in range(n_pages):
        slug_path = html_base_path + '/' + tag_slug
        try:
            os.makedirs(slug_path)
        except OSError:
            pass
        if page == 0:
            page_url = tag_url_base + tag_slug
        else:
            page_url = tag_url_base + tag_slug + '?page=' + str(page + 1)
        html_path = slug_path + '/' + tag_slug + '_' +  str(page + 1) + ".html"
        r = requests.get(page_url)
        time.sleep(0.5)
        if r.status_code == 200:
            with open(html_path, 'wb') as hpfh:
                hpfh.write(r.content)
                
def get_game_list_from_single_tag_page(tag_slug, page_number):
    url = "https://itch.io/games/newest/tag-{}?page={}".format(tag_slug, page_number)
    r = requests.get(url)
    rt = r.text
    soup = bs(rt, "lxml")
    game_divs = soup.find_all("div", class_='game_cell')
    game_id_list = list()    
    for cell in game_divs:
        game_id = cell['data-game_id']
        game_id_list.append(game_id)
    return game_id_list
    
def get_game_info(game_list, game_dir):

# given a list of filenames and a dir, returns a list of tuples
# should probably add game id and game url to return vals
# the bs stuff looks pretty hairy but it seems to work all the time?
# maybe it should write to a CSV or something instead of returning vals

    game_details = list()    
    for game_file in game_list:
        game_id = int(game_file[:-5])
        game_path = game_dir + "/" + game_file
        with open (game_path, 'r') as gfh:
            gt = gfh.read()
        gsoup = bs(gt, "lxml")
        fulltext = gsoup.body.get_text()
        # fulltext = list(gsoup.stripped_strings)
        
        # wtfwtf! no title?
        if gsoup.title:
            title_txt_full = gsoup.title.string
        else:
            title_txt_full = 'wtf, no title?'
        footer_div = gsoup.find('div', id='view_game_footer')
        
        # fuck, some pages don't have footers
        # well only five out of 2600, huh. 
        if footer_div:
            footer_anchors = footer_div.findAll('a')
            creator_url = footer_anchors[2]['href']
            view_all_txt = footer_anchors[2].get_text()
            game_url = footer_anchors[4]['data-lightbox_url'][:-6]
            creator_txt = view_all_txt[12:]
            title_txt = title_txt_full[:-(len(creator_txt) + 4)]
        else:
            title_txt = title_txt_full
            creator_txt = 'no footer!'
            creator_url = 'urg urg urg'
            game_url = 'eff these guys'
        
        game_tup = (game_id, title_txt, creator_txt, creator_url, game_url, fulltext)
        game_details.append(game_tup)
    return game_details

def get_post_info(post_list, post_dir):
# given a list of filenames and a dir, returns a list of tuples

    post_details = list()    
    for post_file in post_list:
        post_id = int(post_file[:-5])
        post_path = post_dir + "/" + post_file
        with open (post_path, 'r', encoding="ISO-8859-1") as pfh:
            pt = pfh.read()
        psoup = bs(pt, "lxml")
        
        trail_anchors = psoup.find_all('a', class_='trail')
        trail_anchor_count = len(trail_anchors)
        if trail_anchor_count > 0:
            trail_anchor_zero = trail_anchors[0]
        else:
            trail_anchor_zero = ''        
        
        post_divs = psoup.find_all('div', class_='post_content')        
        post_div_count = len(post_divs)     
        if post_div_count > 0:
            div_zero = post_divs[0]
            div_zero_length = len(div_zero.getText())
            dz_spans = div_zero.find_all('span')
            dz_span_count = len(dz_spans)
            if dz_span_count > 2:
                # dz_span_a = dz_spans[0].string
                # dz_span_b = dz_spans[1]['title']
                # actually maybe just leave all that stuff in there
                dz_span_a = dz_spans[0]
                dz_span_b = dz_spans[1]
        else:
            div_zero = 'zip'
            div_zero_length = 0  
            dz_span_count = 0
            div_zero = 'zilcho, 404 probs'         
            dz_span_a = ''
            dz_span_b = ''
        
        post_tup = (post_id, trail_anchor_count, trail_anchor_zero, post_div_count, div_zero_length, dz_span_count, dz_span_a, dz_span_b)
        post_details.append(post_tup)
    return post_details

def gamelist(url):

    r = requests.get(url)
    rt = r.text
    # print(rt)
    soup = bs(rt, "lxml")
    lclass = "title game_link"
    allanc = soup.find_all("a", class_=lclass)
    # print(allanc)
    lset = set()
    for anc in allanc:
        lset.add(anc.get_text())
    return list(lset)

def taglist(url):
    # note this is for "top tags", not sure what the cutoff is
    r = requests.get(url)
    rt = r.text
    # print(rt)
    soup = bs(rt, "lxml")
    tclass = "outline_button"
    allanc = soup.find_all("a", class_=tclass)
    # print(allanc)
    tset = set()
    for anc in allanc:
        txt = anc.get_text()
        href = anc['href']
        lab = anc['data-label']
        ttup = (txt, href, lab)
        tset.add(ttup)
    return list(tset)

def tagscrape(taglist):
    tbase = "https://itch.io"
    tclist = list()
    for tag in taglist:
        turl = tbase + tag[1]
        r = requests.get(turl)
        rt = r.text
        # print(rt)
        soup = bs(rt, "lxml")
        cclass = "game_count"
        gcount = soup.find("nobr", class_=cclass)
        gctxt = gcount.get_text()
        gcdig = u''.join(c for c in gctxt if '0' <= c <= '9')
        gctup = (tag[0], tag[1], gcdig, tag[2])
        tclist.append(gctup)
    return tclist

def game_list_from_file(file_path):
    """

    given a file path, returns a list of tuples containing the game name, url, and id    
    the id is unique as far as i can tell
    
    """    
    
    with open (file_path, 'r') as fh:
        rt = fh.read()
    soup = bs(rt, "lxml")
    lclass = "title game_link"
    allanc = soup.find_all("a", class_=lclass)
    # print(allanc)
    lset = set()
    for anc in allanc:
        txt = anc.get_text()
        href = anc['href']
        lab = anc['data-label']
        gid = lab.split(':')
        ltup = (int(gid[1]), txt, href)
        # insert into db        
        # cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
        lset.add(ltup)
    return list(lset)
    
def insert_game_into_db(game_list, db_connection):
    """
    
    takes a list of tuples and a db connection, inserts into a db
    if it takes a long time it might be because it's getting a set of game_id items 
    for every batch of INSERTs, it was either that or make a bunch of try/except blocks
    to skip duplicate game ids. still not sure what the best way to go about that is 
    if your data is sloppy/lazy
    
    """
    cur = db_connection.cursor()
    cur.execute('SELECT game_id FROM itch_game')
    id_result = cur.fetchall()
    id_set =  set([item for sublist in id_result for item in sublist])
    for item in game_list:
        if item[0] not in id_set:
            cur.execute("INSERT INTO itch_game (game_id, name, url) VALUES (%s, %s, %s)", item)
            db_connection.commit()
    cur.close()

def update_tag_associations(game_list, tag_id, db_connection):
    cur = db_connection.cursor()
    cur.execute('SELECT game_id FROM itch_tag_assignments WHERE tag_id=%s', (tag_id, ))
    tag_asses = cur.fetchall()
    tag_ass_set =  set([item for sublist in tag_asses for item in sublist])
    for new_ass in game_list:
        if int(new_ass) not in tag_ass_set: 
            cur.execute("INSERT INTO itch_tag_assignments (game_id, tag_id) VALUES (%s, %s)", (new_ass, tag_id))
            db_connection.commit()
    cur.close()


def info_from_game_page_file(file):
    with open (file, 'r') as fh:
        rt = fh.read()
    soup = bs(rt, "lxml")
    dclass = "post_content"
    alldiv = soup.find_all("div", class_=dclass)
    # print(allanc)
    lset = set()
    for div in alldiv:
        txt = div.get_text()
        print(txt)
    return list(lset)