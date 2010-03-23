from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
	url(r'^reg$', 'reg', name='reg'),
	url(r'^profile$', 'my', name='my'),
	url(r'^space/(?P<user_id>\d+)/$', 'space', name='space'),
	url(r'^edit$', 'edit', name='edit'),
	url(r'^editMore$', 'editMore', name='editMore'),
	url(r'^friends', 'friends', name='friends'),
)