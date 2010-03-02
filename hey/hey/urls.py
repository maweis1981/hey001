from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'hey.users.views.index'),    
    (r'^user/', include('hey.users.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),    

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^photologue/', include('photologue.urls')),
    (r'^avatar/', include('hey.avatar.urls')),
    (r'^avatar_crop/', include('hey.avatar_crop.urls')),
    url(r'^accounts/login/', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', name='auth_logout'),
#    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/avatar/change/'}),

)