from django.conf.urls.defaults import *

urlpatterns = patterns('groups.views',
    url(r'^request$', 'requestFriend', name='requestFriend'),
    url(r'^request$', 'approveFriendRequest', name='approveFriendRequest'),
    url(r'^myRequestFriends$','myRequestFriends',name='myRequestFriends'),
    url(r'^approveRequest$','approveFriendRequest',name='approveFriendRequest'),
    url(r'^myFriends$','myFriends',name='myFriends'),
    url(r'^friends/$','myFriendList',name='myFriendList'),
    url(r'^waitings/$','myRequestFriendsList',name='myRequestFriendsList'),
    url(r'^add/$','addFriend',name='addFriend'),
    url(r'^sendRequest/$','requestFriendInWeb',name='requestFriendInWeb'),
    url(r'^search/([^/]+)','searchUser',name='searchUser'),
    url(r'^find$','searchFriend',name='searchFriend'),
)