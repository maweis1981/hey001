#!/usr/bin/env python
# encoding: utf-8

import os
import re

folderlist = os.listdir('/Users/peter/Public/books')


for f in folderlist:
    print f
    try:
        m = re.match(r"(\d+)-(.*)：(.*)", f, re.S)
        oldName = '/Users/peter/Public/books/%s' % f
        newName = '/Users/peter/Public/books/%s-%s' % (m.group(1), m.group(3))
        print oldName
        print newName
        os.rename(oldName,newName)
    except Exception as msg:
        print msg
        continue
    