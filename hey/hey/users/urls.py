from django.conf.urls.defaults import *

urlpatterns = patterns('',          
     (r'^my/(?P<user_id>\d+)/$', 'hey.users.views.my'),
     (r'^edit/(?P<user_id>\d+)/$', 'hey.users.views.edit'),
     (r'^view/(?P<user_id>\d+)/$', 'hey.users.views.view'),     
     (r'^reg$', 'hey.users.views.reg'),
     (r'^xhr_test$', 'hey.users.views.xhr_test'),
        )
