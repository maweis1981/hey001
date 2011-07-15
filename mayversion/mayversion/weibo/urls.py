from django.conf.urls.defaults import *

urlpatterns = patterns('weibo.views',
    url(r'^oauth$','weiboauth',name='weiboauth'),
    url(r'^accessToken$','accessToken',name='access_token'),
    url(r'^queryToken$','queryAccessToken',name='query_access_token'),
    url(r'^send/([^/]+)$','testSendWeibo',name='test_send_weibo'),
)