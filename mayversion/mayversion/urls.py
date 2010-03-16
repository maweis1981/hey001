from django.conf.urls.defaults import *

import accounts.urls
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mayversion/', include('mayversion.foo.urls')),
    (r'^$', 'accounts.views.my'),
    (r'^accounts/', include('accounts.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^chat/', include('chat.urls')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^avatar/', include('avatar.urls')),
    (r'^avatar_crop/', include('avatar_crop.urls')),

    url(r'^accounts/login/', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', name='auth_logout'),

)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
