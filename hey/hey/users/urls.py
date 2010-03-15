from django.conf.urls.defaults import *

urlpatterns = patterns('hey.users.views',
     url(r'^my$', 'my',name='my'),
     url(r'^edit/(?P<user_id>\d+)/$', 'edit',name='edit'),
     url(r'^edit$', 'editself',name='editself'),
     url(r'^view/(?P<user_id>\d+)/$', 'view',name='view'),
     url(r'^reg$', 'reg',name='reg'),
     url(r'^fillmore$', 'fillmore',name='fillmore'),
     url(r'^xhr_test$', 'xhr_test',name='xhr_test'),
     url(r'^login$', 'login',name='user_login'),
     url(r'^logout$', 'logout',name='user_logout'),
        )
