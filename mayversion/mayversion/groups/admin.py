from django.contrib import admin
from groups.models import FriendRequest,Friends

class FriendRequestAdmin(admin.ModelAdmin):
    pass
class FriendsAdmin(admin.ModelAdmin):
    pass

admin.site.register(FriendRequest,FriendRequestAdmin)
admin.site.register(Friends,FriendsAdmin)