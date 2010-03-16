from django.conf.urls.defaults import *

urlpatterns = patterns('datings.views',
    url(r'^detail/(?P<dating_id>\d+)/$', 'detail', name='dating_detail'),
)