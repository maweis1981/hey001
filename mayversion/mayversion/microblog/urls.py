from django.conf.urls.defaults import *

urlpatterns = patterns('microblog.views',
    url(r'^index$', 'personal', name='tweets_you_follow'),
    url(r'^ajaxTweetSend$', 'ajaxTweetSend', name='tweets_ajax_send'),
    url(r'^ajaxTweetList$', 'ajaxTweetList', name='tweets_ajax_list'),
    url(r'^ajaxPublicTweetList$', 'ajaxPublicTweetList', name='public_tweets_ajax_list'),
    url(r'^all/$', 'public', name='all_tweets'),
    url(r'^(\d+)/$', 'single', name='single_tweet'),
    url(r'^xhr$', 'xhr', name='xhr'),
    url(r'^followers/(\w+)/$', 'followers', name='tweet_followers'),
    url(r'^following/(\w+)/$', 'following', name='tweet_following'),

    url(r'^toggle_follow/(\w+)/$', 'toggle_follow', name='toggle_follow'),
)
