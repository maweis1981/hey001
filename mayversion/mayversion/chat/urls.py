from django.conf.urls.defaults import *

urlpatterns = patterns('chat.views',
url(r'^join/(?P<nick>[\w\-_]+)/', 'add_nick',name='add_nick'),
url(r'^send/(?P<nick>[\w\-_]+)/(?P<msg>.*)/', 'send_msg',name='send_msg'),
url(r'^/?$', 'chat_page',name='chat'),
)