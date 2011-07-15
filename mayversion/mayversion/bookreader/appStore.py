# coding: utf-8
#!/usr/bin/env python
# encoding: utf-8
"""
appStore.py

Created by peter on 2010-03-29.
Copyright (c) 2010 __maweis.com__. All rights reserved.
"""

import re
import urllib
import os
import json
import time

class SinaRead():
    def get_book_title(self,html):
        title = re.findall(r'<h1>(.*?)</h1>', html, re.S)
        return title[0]

    def get_book_cover(self,html):
        cover_path = re.findall(r'''<div class="artwork"><img src="(.*?)" width="175" class="artwork"''', html, re.S)
        return cover_path[0]

    def get_book_description(self,html):
        blocks = re.findall(r'''<div more-text="More" class="product-review" metrics-loc="Titledbox_Description">(.*?)</div>''', html, re.S)
        description = re.findall(r'<p>(.*?)</p>',blocks[0],re.S)
        return description[0]

    def get_book_screenshots(self,html):
        m = re.findall('''<div metrics-loc="iPad" num-items="1" class="content ipad-screen-shots"><div><div class="lockup"><img src="(.*?)" alt="iPad Screenshot 1" class="portrait" /></div></div></div>''', html, re.S)
        return m[0]

    def url_get(self,url):
        u = urllib.urlopen(url)
        html = u.read()
        # c = html.decode('gb2312','ignore').encode('utf8')
        u.close()
        return html


if __name__ == '__main__':
    sinaBook = SinaRead()
    html = sinaBook.url_get('http://itunes.apple.com/us/app/id430162357?mt=8')
    print sinaBook.get_book_title(html)
    print sinaBook.get_book_cover(html)
    print sinaBook.get_book_description(html)
    print sinaBook.get_book_screenshots(html)
 
 

