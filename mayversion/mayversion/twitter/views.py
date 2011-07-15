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

import settings
from datetime import datetime, timedelta
from twitter.models import TwitterAccessToken
from reminds.models import UserDeviceToken
#-------------------------------------------------------

import oauth2 as oauth
import twitter_apis

# parse_qsl moved to urlparse module in v2.6
try:
    from urlparse import parse_qsl
except:
    from cgi import parse_qsl

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

consumer_key    = 'NYqIbv9vCijVb2B6x7jhHg'
consumer_secret = 'fwqThazPj8UGUoEHgErQWjrePssvEdnYpHFuYLfL7jw'


    #
    # Consumer key    NYqIbv9vCijVb2B6x7jhHg
    # Consumer secret    fwqThazPj8UGUoEHgErQWjrePssvEdnYpHFuYLfL7jw
    # Your Twitter Access Token key: 15156279-cNIaX8mVECVTq70MXMvhihkVoGVHwmeTagrpsr0Wa
    #           Access Token secret: 0eO5UwYAQG4JwqRPhYcdwdet2I8BDAgUIV4xWm2SKS4

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
oauth_consumer             = oauth.Consumer(key=consumer_key, secret=consumer_secret)
oauth_client               = oauth.Client(oauth_consumer)


def twitteroauth(request):
    ## check the user_id has already access token yet.
    ###获得应用的token
    ###获得用户OAuth登录的url

    user = User.objects.get(pk=request.GET['user_id'])
    tokens = TwitterAccessToken.objects.filter(user = user)
    if  (len(tokens) == 1):
        return HttpResponse('{result:hasTwitterAccessToken}')

    resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'GET')

    if resp['status'] != '200':
        print 'Invalid respond from Twitter requesting temp token: %s' % resp['status']
        return HttpResponse('{result:error}')
    else:
        request_token = dict(parse_qsl(content))
        print request_token
        request.session['oauth_token'] = request_token['oauth_token']
        request.session['oauth_token_secret'] = request_token['oauth_token_secret']
        auth_url = '%s?oauth_token=%s' % (AUTHORIZATION_URL, request_token['oauth_token'])

        request.session['token'] = request.GET['token']
        print request.session['token']
        return HttpResponseRedirect(auth_url)

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

    try:
        # token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        # token.set_verifier(pincode)
        token = oauth.Token(request.GET['oauth_token'], request.session['oauth_token_secret'])
        oauth_client  = oauth.Client(oauth_consumer, token)
        resp, content = oauth_client.request(ACCESS_TOKEN_URL, method='POST', body='oauth_verifier=%s' % request.GET['oauth_verifier'])
        access_token  = dict(parse_qsl(content))
        if resp['status'] != '200':
            print 'The request for a Token did not succeed: %s' % resp['status']
            print access_token
        else:
            print 'Your Twitter Access Token key: %s' % access_token['oauth_token']
            print '          Access Token secret: %s' % access_token['oauth_token_secret']
            print ''
            token = request.session['token']
            devices = UserDeviceToken.objects.filter(deviceToken=token)
            if (len(devices) == 1):
                tat = TwitterAccessToken()
                tat.user = devices[0].reminder
                tat.key = access_token['oauth_token']
                tat.secret = access_token['oauth_token_secret']
                tat.screen_name = access_token['screen_name']
                tat.twitter_user_id = access_token['user_id']
                tat.save()
                return HttpResponse('{result:twitterTokenSaved}')
            else:
                return HttpResponse('{"result":"twitter token overlimits"}')
    except:
        return HttpResponse('{result:twitter api error}')

    # ###发布微博
    # api = API(auth)
    # status = api.update_status(status="binding Arrived.")
    return HttpResponse('{result:twitter oauth done.}')

def queryAccessToken(request):
    user = User.objects.get(pk=request.GET['user_id'])
    tokens = TwitterAccessToken.objects.filter(user = user)
    if  (len(tokens) == 1):
        print tokens[0]
        return HttpResponse('{"result":"done"}')
    return HttpResponse('{"result":"error"}')


def testSendTweet(request,message):
    user = User.objects.get(pk=2)
    tokens = TwitterAccessToken.objects.filter(user = user)
    api = twitter_apis.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                         access_token_key=tokens[0].key, access_token_secret=tokens[0].secret,
                         input_encoding='UTF-8')
    
    status = api.PostUpdate('%s [%s]' % (message,datetime.now()))
    return HttpResponse('{"result":"%s"}' % status)


