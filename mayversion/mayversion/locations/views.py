#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, get_list_or_404
from locations.models import Location
from reminds.models import Remind, RemindLocation, REMINDS_STATUS, RemindSendResult
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core import serializers
from django.db import models, connection
from decimal import *

from decimal import *
from apns import APNs, Payload
import settings

from django.db.models import Q

import math
import simplejson as json
import urllib

from weibopy.auth import OAuthHandler
from weibopy.api import API
from weibo.models import WeiboAccessToken

import oauth2 as oauth
import twitter_apis
from twitter.models import TwitterAccessToken

from django.utils.timesince import timesince
from datetime import datetime, timedelta

import settings

nauticalMilePerLat = 60.00721
nauticalMilePerLongitude = 60.10793
rad = math.pi / 180.0
milesPerNauticalMile = 1.15078
kilometersPerMiles = 1.60931

def sendTweet(user_id, message):
    user = User.objects.get(pk=user_id)
    tokens = TwitterAccessToken.objects.filter(user=user)
    if len(tokens) > 0:
        api = twitter_apis.Api(consumer_key=settings.consumer_key, consumer_secret=settings.consumer_secret,
                               access_token_key=tokens[0].key, access_token_secret=tokens[0].secret,
                               input_encoding='UTF-8')
        status = api.PostUpdate('%s [%s]' % (message, datetime.now()))
    else:
        pass


def sendWeibo(user_id, message):
    auth = OAuthHandler(settings.WEIBO_APP_KEY, settings.WEIBO_APP_SECRET)
    ###获得access_token后,以后便可以通过
    #get the access info from database by user_id
    user = User.objects.get(pk=user_id)
    weibo = WeiboAccessToken.objects.filter(user=user)
    if (len(weibo) > 0):
        auth.set_access_token(weibo[0].key, weibo[0].secret)
        ###完成授权.
        api = API(auth)
        weibo_msg = '%s [%s]' % (message, datetime.now())
        status = api.update_status(status=weibo_msg)
    else:
        pass


def getAround(lat, lon, radius):
    lat = float(lat)
    lon = float(lon)
    radius = float(radius)
    #exchange NM
    radius = (radius / 1000) / kilometersPerMiles / milesPerNauticalMile
    print radius
    dpmLat = 1 / nauticalMilePerLat
    radiusLat = dpmLat * radius
    minLat = lat - radiusLat
    maxLat = lat + radiusLat

    mpdLng = nauticalMilePerLongitude * math.cos(lat * rad)
    dpmLng = 1 / mpdLng
    radiusLng = dpmLng * radius
    minLng = lon - radiusLng
    maxLng = lon + radiusLng
    return [minLat, minLng, maxLat, maxLng]


def calcDistance(lat1, lon1, lat2, lon2):
    """
     Caclulate distance between two lat lons in NM
     """
    print 'calc distance %s,%s--%s,%s' % (lat1, lon1, lat2, lon2)
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    yDistance = (lat2 - lat1) * nauticalMilePerLat
    xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * (nauticalMilePerLongitude / 2)
    distance = math.sqrt(yDistance ** 2 + xDistance ** 2)
    print 'distance is %s' % (distance * milesPerNauticalMile * kilometersPerMiles)
    return distance * milesPerNauticalMile * kilometersPerMiles


def getAddress(lat, lon, language):
    url = 'http://maps.google.com/maps/api/geocode/json?latlng=%s,%s&sensor=false&language=%s' % (lat, lon, language)
    u = urllib.urlopen(url)
    content = u.read()
    u.close()
    contentObj = json.loads(unicode(content, "UTF-8"))
    # print url
    # print contentObj
    # print contentObj['results'][0]['formatted_address']
    return contentObj['results'][0]['formatted_address']


def getGeo(address, language):
    url = 'http://maps.google.com/maps/api/geocode/json?address=%s&sensor=true&language=%s' % (
    address.encode('utf-8'), language)
    u = urllib.urlopen(url)
    content = u.read()
    u.close()
    contentObj = json.loads(unicode(content, "UTF-8"))
    return (
    contentObj['results'][0]['geometry']['location']['lat'], contentObj['results'][0]['geometry']['location']['lng'])


def nearbyUser(request, user_id):
    tempUser = get_object_or_404(User, pk=user_id)
    location = Location.objects.filter(user=tempUser).order_by('id')[:1]
    print location
    location = location[0]
    scopes = getAround(location.latitude, location.longitude, 1000)
    query = ("select distinct(user_id),latitude,longitude,date from locations_location where latitude > %(minLat)f"
             " and latitude < %(maxLat)f and longitude > %(minLng)f and longitude < %(maxLng)f group by user_id order by id desc") % {
        'minLat': scopes[0],
        'maxLat': scopes[2],
        'minLng': scopes[1],
        'maxLng': scopes[3],
        }
    print query
    cursor = connection.cursor()
    nearby_ids = cursor.execute(query)
    nearbyList = []
    for v in cursor.fetchall():
        print v
        nearbyList.append(User.objects.get(pk=int(v[0])))
    print len(nearbyList)
    if len(nearbyList) == 0:
        return HttpResponse('not found')
    else:
        response = HttpResponse(mimetype="text/javascript")
        serializers.serialize("json", nearbyList, stream=response)
        return response


def location_by_user(request, username):
    tempUser = get_object_or_404(User, username=username)
    location_list = get_list_or_404(Location, user=tempUser)
    return render_to_response('location/location_by_user.html', locals())


def location_by_user_json(request):
    if request.method == "POST":
        tempUser = get_object_or_404(User, username=request.POST['username'])
        location_list = get_list_or_404(Location, user=tempUser)
        response = HttpResponse(mimetype="text/javascript")
        serializers.serialize("json", location_list, stream=response)
        return response

    return HttpResponse(request.META('USER-AGENT'))


def addLocationRemindScope(request):
    return render_to_response('location/pickLocation.html', locals())


def searchLocationByAddress(request, address):
    # print request.GET.get('address')
    geo = getGeo(address, 'en_US')
    return HttpResponse("%s %s %s " % (address, geo[0], geo[1]))
    # geo = getGeo(address,'zh_CN')
    # return HttpResponse('{lat:%s,lng:%s}' % (geo[0],geo[1]))


def commitLocation(request):
    if request.method == "POST":
        if request.POST['latitude']:
            location = Location()
            user = User.objects.get(pk=request.POST['user_id'])
            location.user = user
            location.latitude = Decimal(request.POST['latitude'].strip())
            location.longitude = Decimal(request.POST['longitude'].strip())
            addressStr = getAddress(location.latitude, location.longitude, 'en_US')
            location.address = addressStr
            #check the location exist?
            existLocations = Location.objects.filter(address__contains=addressStr, user=user,
                                                     latitude=location.latitude,
                                                     longitude=location.longitude,
                                                     ).order_by('-date')
            existFlag = True

            if len(existLocations) > 0:
                print (datetime.now() - existLocations[0].date).seconds
                print timesince(existLocations[0].date)
                if  ((datetime.now() - existLocations[0].date).seconds < 60 * 60):
                    existFlag = False
                    # 1 hour = 60 minutes 1 hour could not be upload the same location

            # add Q query for OR to get the first notification & always notification
            if existFlag:
                location.save()
                reminds = Remind.objects.filter(Q(status=0) | Q(status=1))
                # reminds = Remind.objects.all()
                for remind in reminds:
                    print remind.invitee
                    if remind.location:
                        if calcDistance(location.latitude, location.longitude, remind.location.latitude,
                                        remind.location.longitude) < 1.5:
                            apns = APNs(use_sandbox=True, cert_file=settings.APNS_CERTIFICATE,
                                        key_file=settings.APNS_KEY)
                            payload = Payload(alert=remind.subject, sound="default", badge=1)
                            print 'remind will be send'
                            weibo_msg = ''

                            for inv in remind.invitee.all():
                                print 'reminder = %s' % inv.reminder
                                print weibo_msg
                                apns.gateway_server.send_notification(inv.deviceToken, payload)
                                print 'send notification yet'
                                weibo_msg = '%s,%s' % (remind.subject, remind.location.description)
                                print 'weibo_msg value set.'
                                weibo_inviters = WeiboAccessToken.objects.filter(user=inv.reminder)
                                if (len(weibo_inviters) > 0):
                                    for inviter in weibo_inviters:
                                        weibo_msg = '%s @%s' % (weibo_msg, inviter.screen_name)
                                        print 'weibo_msg setting....'
                                        # sendWeibo(inv.reminder.id,weibo_msg)
                            sendWeibo(user.id, weibo_msg)
                            print 'send weibo yet'
                            sendTweet(user.id, weibo_msg)
                            print 'send tweet yet'
                            #update status by just once or always
                            if remind.status == 0: #just once
                                remind.status = 3
                                remind.save()
                            remindSendResult = RemindSendResult()
                            remindSendResult.remind = remind
                            remindSendResult.save()
                            return HttpResponse('{"result":"send push done"}')
                        else:
                            print 'distance big more 1'
                    return HttpResponse('{result:ok}')
            else:
                return HttpResponse('{result:alreadyExist}')
    else:
        return HttpResponse('{result:noPOST}')


def addRemindLocation(request):
    if request.method == "POST":
        if request.POST['latitude']:
            user = get_object_or_404(User, username=request.POST['username'])
            remindLocation = RemindLocation()
            remindLocation.creater = user
            remindLocation.latitude = Decimal(request.POST['latitude'].strip())
            remindLocation.longitude = Decimal(request.POST['longitude'].strip())
            if  request.POST['description']:
                remindLocation.description = request.POST['description']
            else:
                remindLocation.description = getAddress(remindLocation.latitude, remindLocation.longitude, 'zh_CN')

            remindLocation.save()
            return HttpResponse('{result:ok}')
        else:
            return HttpResponse('{result:noData}')
    else:
        return HttpResponse('{result:noPOST}')
    
