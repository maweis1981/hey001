from django.conf.urls.defaults import *

urlpatterns = patterns('twitter.views',
    url(r'^oauth$','twitteroauth',name='twitter_boauth'),
    url(r'^accessToken$','accessToken',name='access_token'),
    url(r'^queryToken$','queryAccessToken',name='query_access_token'),
    url(r'^send/([^/]+)$','testSendTweet',name='test_send_tweet'),
)