#!/usr/bin/env python
# encoding: utf-8
"""
SinaReader.py

Created by peter on 2010-03-29.
Copyright (c) 2010 __maweis.com__. All rights reserved.
"""

import re
import urllib
import os
import json
import stomp
import time
import settings
from bookreader.models import Book

class SinaRead():
    def get_book_title(self,html):
        title = re.findall(r'<h1>(.*?)</h1>', html, re.S)
        return title[0]

    def get_book_cover(self,html):
        cover_path = re.findall(r'''<div class="pic" style="float:left;"><img src="(.*?)" width="200"''', html, re.S)
        return cover_path[0]

    def extract_links(self,html):
        blocks = re.findall(r'<ul class="list_009">.*?</ul>', html, re.S)
        links = []
        for b in blocks:
            links += re.findall(r'<a href="(\S+)"[^<>]*>([^<>]*)</a>', b)
        return links

    def extract_content(self,html):
        m = re.search('<div id="contTxt" class="contTxt1">.*<p class="pages"><script>', html, re.S)
        return m and self.html_to_text(m.group()) or ''

    def html_to_text(self,html):
        html = re.sub(r'<p>(.*?)</p>', r'\1\n', html)
        html = re.sub(r'<[^<>]*>', '', html)
        return "\n\n" + html.strip() + "\n\n"


    def url_get(self,url):
        u = urllib.urlopen(url)
        html = u.read()
        c = html.decode('gb2312','ignore').encode('utf8')
        u.close()
        return c


    def pushToStomp(self,conn, msg):
        o = {"message": msg,"time":time.strftime("%Y-%m-%d %X", time.gmtime())}
        msg_to_send = json.dumps(o)
#        print msg_to_send
#        conn.send(msg_to_send, destination= 'bookreader')

    def connectToStomp(self):
#        try:
#            conn = stomp.Connection([(settings.ORBITED_SERVER, 61613)], 'guest', 'guest')
#            conn.start()
#            conn.connect()
#
#        except Exception as msg:
#            print msg
#            conn.send('Exception [%s]' % msg, destination= 'bookreader')
        conn = ''
        return conn

    def download_book(self,urlindex, bookId,bookTitle):
        conn = self.connectToStomp()

        # self.pushToStomp(conn,'get book  %s' % bookId)
        content = self.url_get(urlindex)

        # self.pushToStomp(conn,'get book title %s '% bookTitle)

        # self.pushToStomp(conn, 'get book cover <img src="%s"/> '% coverPath)

        links = self.extract_links(content)

        # self.pushToStomp(conn,'get book capters , book has %s capters '% len(links))

        # self.pushToStomp(conn,'保存书籍 [' + bookTitle + ']' + str(bookId))

        folderName = settings.BOOKS_ROOT + '/' + str(bookId) + '-' + bookTitle + '/'
        # self.pushToStomp(conn,'创建目录'+folderName)

        if not os.path.exists(folderName):
            os.makedirs(folderName)
            # self.pushToStomp(conn,'创建成功')
        # else:
            # self.pushToStomp(conn,'目录已经存在')

        os.chdir(folderName)
        # self.pushToStomp(conn,'进入目录')
        try:
            fp = open("%s.txt" % bookTitle, 'w')
        # self.pushToStomp(conn,'create text file ...')
            capterNum = 0
            for link in links:
                u = 'http://vip.book.sina.com.cn/book/' + link[0]
                title = link[1]
                fp.write(title)

                capterNum = capterNum + 1
            # self.pushToStomp(conn,'storing book %s ' % title.encode('utf-8'))
                print '保存书籍 %s ' % title
                try:
                    capterp = open("("+str(capterNum)+")-%s.txt" % title, 'w')
                    capterp.write(title)
                    print u
                    capterContent = self.url_get(u)
                    capterp.write(self.extract_content(capterContent))
                    capterp.close()
                    fp.write(self.extract_content(capterContent))
                except Exception as msg:
                    print msg
                
            # self.pushToStomp(conn,'stored capter %s ' % title.encode('utf-8'))

            fp.close()
        except Exception as errMsg:
            print 'Error [%s]' % errMsg
        # self.pushToStomp(conn,'stored book  %s ' % bookTitle)
        # bookFolderName = str(bookId) + '-' + bookTitle
        # self.pushToStomp(conn,'stored book <a href="http://192.168.0.2/books/'+ bookFolderName +'/">'+ bookTitle +'</a>')

    def download_book_by_id(self,bookId,bookTitle):
        self.download_book('http://vip.book.sina.com.cn/book/index_%s.html' % bookId, bookId,bookTitle)


    def get_book_ids(self,list_page_content):
        title = re.findall(r'<li>(.*?)</li>', list_page_content, re.S)
        for t in title:
            b_id = ''
            b_url = ''
            b_title = ''
            b_authro = ''
            b_pub_house = ''
            b_description = ''
            b_cover_url = ''
            b_pub_date = ''

            book_name_content = re.findall(r'<h2>(.*?)</h2>', t , re.S)[0]
            book_link = re.findall(r'<a href="(.*?)" target', book_name_content , re.S)
            b_url = book_link[0]

            sinaBookId = re.findall(r'http://vip.book.sina.com.cn/book/index_(\d+).html', book_link[0],re.S)
            if len(sinaBookId) > 0:
                b_id = sinaBookId[0]
            else:
                continue

            book_name = re.findall(r'target="_blank">(.*?)</a>', book_name_content , re.S)
            b_title = book_name[0]


            book_description = re.findall(r'<p>(.*?)</p>', t , re.S)
            b_description = book_description[0]

            book_cover = re.findall(r'<img src="(.*?)"', t, re.S)
            b_cover_url = book_cover[0]

            book_author = re.findall(r'<a href=".*?" target="_blank" class="f12black">(.*?)</a>',t,re.S)
            b_author = book_author[0]
            b_pub_house = book_author[1]
            book_pub_time = re.findall(
                    r'<span style="display:block;float:left;width:180px;height:20px;line-height:20px;overflow:hidden;">出版时间：(.*?)</span>'
                    , t, re.S)
            if len(book_pub_time) > 0:
                b_pub_date = book_pub_time[0]

            book = Book(book_id=b_id,
                        book_url = b_url,
                        title = b_title,
                        author = b_author,
                        pub_house = b_pub_house,
                        description = b_description,
                        status = 1,
                        cover_url = b_cover_url,
                        pub_date = b_pub_date
                        )
            book.save()
            print book.toString()

            


    def getSinaBookList(self):
        for p in range(1,30076):
            print 'Page [ %s ] ' % p
            url = 'http://vip.book.sina.com.cn/pub/iframe.php?p='+ str(p) +'&t=p&s=list&r=20&o=t&dpc=1'
            c = self.url_get(url)
            self.get_book_ids(c)



    def getSinaBookEntry(self):
        books = Book.objects.filter(status=1).all()
        for b in books:
            print b.title
            self.download_book_by_id(b.book_id,b.title)
            b.status = 2
            b.save()
            print b.title + 'Done.'
            



if __name__ == '__main__':
    sinaBook = SinaRead()
    #    sinaBook.download_book('http://vip.book.sina.com.cn/book/index_96877.html', '96877.txt')
    #    sinaBook.download_book_by_id('127789')
    for p in range(1,35576):
        print p
        url = 'http://vip.book.sina.com.cn/pub/iframe.php?p='+ p +'&t=p&s=list&r=20&o=t&dpc=1'
        c = sinaBook.url_get(url)
        sinaBook.get_book_ids(c)


