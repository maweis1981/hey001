#!/usr/bin/env python
# encoding: utf-8


from django.conf.urls.defaults import *

urlpatterns = patterns('locations.views',
    url(r'^location/([A-Za-z]+)','location_by_user',name='location_by_user'),
    url(r'^nearby/(\d+)$','nearbyUser',name='nearbyUser'),
    url(r'^locationJson$','location_by_user_json',name='location_by_user_json'),
    url(r'^submitLocation/$','commitLocation',name='commit_location_via_device'),
    url(r'^addRemindLocation/$','addRemindLocation',name='add_remind_location_via_device'),
    url(r'^pickLocation/$','addLocationRemindScope',name='pick_location'),
    url(r'^search/([^/]+)','searchLocationByAddress',name='searchLocationByAddress'),
)
