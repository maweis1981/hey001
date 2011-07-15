from django.contrib import admin
from weibo.models import WeiboAccessToken

class WeiboAccessTokenAdmin(admin.ModelAdmin):
    pass

admin.site.register(WeiboAccessToken,WeiboAccessTokenAdmin)
