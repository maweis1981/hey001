from django.contrib import admin
from twitter.models import TwitterAccessToken

class TwitterAccessTokenAdmin(admin.ModelAdmin):
    pass

admin.site.register(TwitterAccessToken,TwitterAccessTokenAdmin)