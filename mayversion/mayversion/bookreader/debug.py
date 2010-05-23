#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by peter on 2010-03-30.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import re
import urllib

from SinaReader import safe_str  ,safe_unicode

def url_get(url):
    print url
    u = urllib.urlopen(url)
    c = unicode(u.read(), 'gb18030') 
#    print safe_unicode(c,"gb2312")
    u.close()
    return c

def get_book_title(html):
    title = re.findall(r'<h1>(.*?)</h1>', html, re.S)
    print title
    print title[0].encode("utf-8")


if __name__ == '__main__':
    str = '<h1>abcdefg</h1>'
    get_book_title(url_get('http://vip.book.sina.com.cn/book/index_96877.html'))

