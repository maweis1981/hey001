from django.shortcuts import render_to_response, get_object_or_404,HttpResponse,get_list_or_404

from reminds.models import UserDeviceToken,Remind,RemindLocation,RemindUserShip,RemindSendResult
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.db.models import Q

from decimal import *
from apns import APNs, Payload
import settings
from django.core import serializers

import simplejson as json

from locations.views import getAddress
from locations.models import Location

from avatar.models import Avatar
from avatar.util import get_primary_avatar, get_default_avatar_url

import settings
    
def registerDeviceToken(request):
    if request.method == "POST":
        if request.POST['token']:
            tokenUser = UserDeviceToken()
            tokenUser.reminder = get_object_or_404(User, username=request.POST['username'])
            tokenUser.deviceToken = request.POST['token']
            tokenUser.save()
            apns = APNs(use_sandbox=True, cert_file=settings.APNS_CERTIFICATE,key_file=settings.APNS_KEY)
            token_hex = tokenUser.deviceToken
            payload = Payload(alert="welcome!", sound="default", badge=1)
            apns.gateway_server.send_notification(token_hex, payload)
            return HttpResponse('{result:ok}')
        else:
            return HttpResponse('{result:noToken}')
    else:
        return HttpResponse('{result:noPOST}')

def MyReminds(request,user_id):
    user = User.objects.get(pk=user_id)
    print user.username
    reminds = Remind.objects.filter(creater=user)
    print len(reminds)
    
    device = UserDeviceToken.objects.filter(reminder = user)
    print device 
    if device:
        deviceReminds = Remind.objects.filter(invitee = device[0])
    
    return render_to_response('reminds/myReminds.html',locals())
        
def createRemind(request):
    # create remind with location & social message
    if request.method == 'POST':
        remind = Remind()
        user = User.objects.get(pk=request.POST['user_id'])
        remind.creater = user
        remind.subject = request.POST['subject']
#check the remind location exists?
        remindLocation = RemindLocation()
        remindLocation.creater = user
        remindLocation.latitude = request.POST['latitude']
        remindLocation.longitude = request.POST['longitude']
#maybe use the user custom address name .
        # remindLocation.description = request.POST['address']
        remindLocation.description = getAddress(remindLocation.latitude,remindLocation.longitude,'en_US')
        remindLocation.mapImg.save('map.jpg',request.FILES['mapImg'])
        
        existLocations = RemindLocation.objects.filter(description__contains=remindLocation.description,creater=user,
                                latitude = remindLocation.latitude,
                                longitude = remindLocation.longitude,
                                ).order_by('-create_date')
        if len(existLocations) == 0:
            remindLocation.save()
        else:
            remindLocation = existLocations[0]
        remind.location = remindLocation
        remind.save()
        
        invitee_ids = request.POST['invitee_id'].split()
        if (len(invitee_ids) == 0 ):
            return HttpResponse('{result:noInviteeFound}')
        for inv_id in invitee_ids:
            inviteer = User.objects.get(pk=inv_id)
            invitee = UserDeviceToken.objects.filter(reminder = inviteer)
            if (len(invitee) > 0):
                rus = RemindUserShip(user = invitee[0],remind=remind)
                rus.save()
        return HttpResponse('{result:done}')
    else:
        return HttpResponse('{result:noPostMethod}')
    
def MyRemindsJSON(request,user_id):
    user = User.objects.get(pk=user_id)
    device = UserDeviceToken.objects.filter(reminder = user)
    if device:
        # reminds = Remind.objects.filter(Q(creater=user) | Q(invitee = device[0]))
        reminds = Remind.objects.filter(Q(invitee = device[0])).order_by('-datetime_create')
    else:
        reminds = Remind.objects.filter(creater=user)
    if(len(reminds) > 0):
        rs = []
        for remind in reminds:
            rem = {}
            rem['subject'] = remind.subject
            rem['datetime_create'] = '%s' % remind.datetime_create
            rem['creater'] = remind.creater.username
            avatar = get_primary_avatar(user,size=40)
            if avatar:
                rem['avatar_url'] = '%s%s' % (settings.APP_SERVER_HOST,avatar.avatar_url(40))
            else:
                rem['avatar_url'] = '%s%s' % (settings.APP_SERVER_HOST,get_default_avatar_url())
            rem['creater_id'] = remind.creater.id
            rem['location'] = remind.location.description
            rem['mapImg'] = '%s/media/%s' % (settings.APP_SERVER_HOST,remind.location.mapImg)
            rem['status'] = remind.status
            
            remindSendResults = RemindSendResult.objects.filter(remind=remind)
            rem['sendCount'] = len(remindSendResults)
            # rem['invitee'] = remind.invitee.all()
            rs.append(rem)
        return HttpResponse(json.dumps(rs))
    return HttpResponse('{result:noData}')

def myRemindLocationsJson(request,user_id):
    user = User.objects.get(pk=user_id)
    remindLocations = RemindLocation.objects.filter(creater=user)
    response = HttpResponse(mimetype="text/javascript")
    serializers.serialize("json", remindLocations, stream=response)
    return response

def myRemindLocations(request,user_id):
    user = User.objects.get(pk=user_id)
    remindLocations = RemindLocation.objects.filter(creater=user)
    return render_to_response('reminds/myRemindLocation.html',locals())

def checkRemind(request,remind_id):
    remind = get_object_or_404(Remind,pk=remind_id)
    apns = APNs(use_sandbox=True, cert_file=settings.APNS_CERTIFICATE,key_file=settings.APNS_KEY)
    payload = Payload(alert=remind.subject, sound="default", badge=1)
    for invit in remind.invitee.all():
        print 'device token is %s' % invit.deviceToken
        apns.gateway_server.send_notification(invit.deviceToken, payload)
    return render_to_response('reminds/remind.html',locals())


def cronRemind(remind_id):
    remind = Remind.objects.get(pk=remind_id)
    apns = APNs(use_sandbox=True, cert_file=settings.APNS_CERTIFICATE,key_file=settings.APNS_KEY)
    payload = Payload(alert=remind.subject, sound="default", badge=1)
    apns.gateway_server.send_notification(remind.invitee.deviceToken, payload)