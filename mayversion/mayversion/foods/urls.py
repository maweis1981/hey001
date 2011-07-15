from django.conf.urls.defaults import *

urlpatterns = patterns('foods.views',
    url(r'^share$','upload',name='upload'),
    url(r'^upload$','uploadPhoto',name='uploadPhoto'),
    url(r'^upload_avatar$','uploadAvatar',name='uploadAvatar'),
    url(r'^list$','showFoods',name='showFoods'),
)