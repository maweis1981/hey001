from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('avatar.views',
    url('^add/(?P<user_id>\d+)/$', 'add', name='avatar_add'),
    url('^change/(?P<user_id>\d+)/$', 'change', name='avatar_change'),
    url('^delete/(?P<user_id>\d+)/$$', 'delete', name='avatar_delete'),
    url('^render_primary/(?P<user>[\+\w]+)/(?P<size>[\d]+)/$', 'render_primary', name='avatar_render_primary'),    
)
