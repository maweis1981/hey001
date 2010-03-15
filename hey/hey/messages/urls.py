from django.conf.urls.defaults import *

urlpatterns = patterns('hey.messages.views',
     url(r'^send/$', 'send', name='message_send'),
     url(r'^send/success$', 'success', name='message_success'),
     url(r'^my/(?P<user_id>\d+)/$', 'myTransferMessages', name='message_my'),
)
