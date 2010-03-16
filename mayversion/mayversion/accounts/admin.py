from django.contrib import admin
from accounts.models import UserProfile,UserMoreProfile,WhoVisitMe

class UserProfileAdmin(admin.ModelAdmin):
    pass

class UserMoreProfileAdmin(admin.ModelAdmin):
    pass

class WhoVisitMeAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserMoreProfile,UserMoreProfileAdmin)
admin.site.register(WhoVisitMe,WhoVisitMeAdmin)



