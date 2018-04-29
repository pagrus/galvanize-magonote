import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import os
import pickle
import boto3
import re
import time

def get_game_info(game_list, game_dir):
    for game_file in game_list:
        game_path = game_dir + "/" + game_file
        with open (game_path, 'r') as gfh:
            gt = gfh.read()
        gsoup = bs(gt, "lxml")
        title_txt_full = gsoup.title.string
        footer_div = gsoup.find('div', id='view_game_footer')
        creator_url = footer_div.findAll('a')[2]['href']
        view_all_txt = footer_div.findAll('a')[2].get_text()
        creator_txt = view_all_txt[12:]
        title_txt = title_txt_full[:-(len(creator_txt) + 4)]
        print(title_txt, creator_txt, creator_url)

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

def gamelist_from_file(file):
    with open (file, 'r') as fh:
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
        ltup = (txt, href, int(gid[1]))
        lset.add(ltup)
    return list(lset)

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