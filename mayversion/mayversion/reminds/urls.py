from django.conf.urls.defaults import *

urlpatterns = patterns('reminds.views',
    url(r'^addDevice/$','registerDeviceToken',name='register_device_token'),
    url(r'^create$','createRemind',name='create_remind'),
    url(r'^checkRemind/(?P<remind_id>\d+)/$','checkRemind',name='check_remind'),
    url(r'^reminds/(?P<user_id>\d+)/$','MyReminds',name='my_remind'),
    url(r'^reminds_json/(?P<user_id>\d+)/$','MyRemindsJSON',name='my_remind_json'),
    url(r'^locations/(?P<user_id>\d+)/$','myRemindLocations',name='my_remind_locations'),
    url(r'^locations_json/(?P<user_id>\d+)/$','myRemindLocationsJson',name='my_remind_locations_json'),
)