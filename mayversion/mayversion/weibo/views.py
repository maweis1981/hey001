#!/usr/bin/python 
#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404,HttpResponse,get_list_or_404

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.db.models import Q

from decimal import *
from apns import APNs, Payload
import settings
from django.core import serializers

import simplejson

from weibopy.auth import OAuthHandler
from weibopy.api import API

import settings

from weibo.models import WeiboAccessToken
from reminds.models import UserDeviceToken
#-------------------------------------------------------
auth = OAuthHandler(settings.WEIBO_APP_KEY, settings.WEIBO_APP_SECRET)

def weiboauth(request):
    ## check the user_id has already access token yet.
    ###获得应用的token
    ###获得用户OAuth登录的url

    user = User.objects.get(pk=request.GET['user_id'])
    tokens = WeiboAccessToken.objects.filter(user = user)
#    if  (len(tokens) == 1):
#        return HttpResponse('{result:hasAccessToken}')
    auth_url = auth.get_authorization_url()
    print auth_url
    request.session['token'] = request.GET['token']
    print request.session['token']
    return HttpResponseRedirect('%s&display=mobile&oauth_callback=arrived://?' % (auth_url))
    # return HttpResponseRedirect('%s&display=mobile&oauth_callback=%s/weibo/accessToken?' % (auth_url,settings.APP_SERVER_HOST))
    # print "Please Auth: "+auth_url
    # verifier = raw_input("PIN: ").strip()
    # access_token = auth.get_access_token(verifier)
    # ###获得access_token
    #
    # ###发布微博
    # api = API(auth)
    # status = api.update_status(status="Hello World")
 
    ###获得access_token后,以后便可以通过
    ###auth.set_access_token(access_token.key, access_token.secret)
    ###完成授权.
def accessToken(request):
    print request.GET['oauth_token']
    print request.GET['oauth_verifier']
    try:
        access_token = auth.get_access_token(request.GET['oauth_verifier'])
        print auth.get_username()
        token = request.session['token']
        devices = UserDeviceToken.objects.filter(deviceToken=token)
        if (len(devices) == 1):
            wat = WeiboAccessToken()
            wat.user = devices[0].reminder
            wat.key = access_token.key
            wat.secret = access_token.secret
            wat.screen_name = auth.get_username()
            wat.save()
            return HttpResponse('{result:tokenSaved}')
        else:
            return HttpResponse('{"result":"token overlimits"}')
    except:
        return HttpResponse('{result:sina weibo api error}')

    # ###发布微博
    # api = API(auth)
    # status = api.update_status(status="binding Arrived.")
    return HttpResponse('{result:done.}')

def queryAccessToken(request):
    user = User.objects.get(pk=request.GET['user_id'])
    tokens = WeiboAccessToken.objects.filter(user = user)
    if  (len(tokens) == 1):
        print tokens[0]
        return HttpResponse('{"result":"done"}')
    return HttpResponse('{result:error}')


def testSendWeibo(request,message):

    # Access token key: fbe5e1a712bc711a6ab9d32d4287c80c
    # Access token secret: 374bdc24eba5aefa0230f2a55ad57a98
    ###获得access_token后,以后便可以通过
    auth.set_access_token('fbe5e1a712bc711a6ab9d32d4287c80c', '374bdc24eba5aefa0230f2a55ad57a98')
    ###完成授权.
    api = API(auth)
    status = api.update_status(status=message)
    return HttpResponse('{result:%s}' % status)


