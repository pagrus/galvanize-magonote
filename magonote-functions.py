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