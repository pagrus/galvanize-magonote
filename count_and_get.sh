import requests
import os
import time

ppdir = "html/post_pages"
test_count = 0
dl_count = 0

post_list = list()
post_set = set(os.listdir(ppdir))

for post in range(2000):
    test_str = str(post) + ".html"
    if test_str in post_set:
        test_count += 1
    else:
        dl_count += 1
        purl = "https://itch.io:443/post/" + str(post)
        dlfile = ppdir + "/" + test_str
        response = requests.get(purl)
        time.sleep(1)
        rt = response.text
        with open(dlfile, "w") as fh:
            fh.write(rt)

print(test_count, dl_count)
