from django.conf.urls.defaults import *

urlpatterns = patterns('messages.views',
     url(r'^send$', 'send', name='message_send'),
     url(r'^send/(?P<user_id>\d+)/$', 'sendToUser', name='message_send_to_someone'),
     url(r'^send/success$', 'success', name='message_success'),
     url(r'^my$', 'myMessages', name='message_my'),
)
