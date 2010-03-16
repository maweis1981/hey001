from django.contrib import admin
from mayversion.accounts.models import UserProfile,UserMoreProfile

class UserProfileAdmin(admin.ModelAdmin):
    pass

class UserMoreProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserMoreProfile,UserMoreProfileAdmin)



