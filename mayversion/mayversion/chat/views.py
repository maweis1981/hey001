from pyorbited.simple import Client

from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse

users = []
orbit = Client()

def chat_page(request, users = users, orbit = orbit):
    return render_to_response('chat/chat.html',locals())

def add_nick(request,nick,users = users,orbit=orbit):
    users.append((nick,'0'))
    orbit.event(user_k(), '%s joined ' % nick)
    return HttpResponse("ok")

def send_msg(request, nick, msg, users = users, orbit=orbit):
    orbit.event(user_k(), '%s %s' % (nick, msg))
    return HttpResponse("ok")

def user_k(uers= users):
    lista = ["%s, %s, /chat" % (user[0],str(user[1]))
            for user in users]
    return lista