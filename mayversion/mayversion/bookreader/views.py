#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render_to_response,HttpResponse

from bookreader.models import Book
from bookreader.SinaReader import SinaRead

import settings
import re
import urllib
import os
import json
import stomp
import time

from django.core.paginator import Paginator, InvalidPage, EmptyPage

def workbench(request):
    return render_to_response('bookreader/copy_book.html', locals())

def copyBookFromSina(request):
    book_id = request.POST['book_id']
    if type(book_id) == int:
        print book_id
    else:
        sinaBookId = re.findall(r'http://vip.book.sina.com.cn/book/index_(\d+).html', book_id,re.S)
        print sinaBookId[0]
        book_id = sinaBookId[0]

    try:
        s = SinaRead()
#    sinaBook.download_book('http://vip.book.sina.com.cn/book/index_96877.html', '96877.txt')
        s.download_book_by_id(book_id)
    except Exception as msg:
        print msg
    return HttpResponse('{result:ok}')

def listBooks(request):
    books = Book.objects.all()
    paginator = Paginator(books, 10)
    
    try:
        page = int(request.GET.get('page', '1'))
    except valueError:
        page = 1
        
    try:
        books = paginator.page(page)
    except (EmptyPage, InvalidPage):
        books = paginator.page(paginator.num_pages)
        
    return render_to_response('bookreader/list.html', locals())
