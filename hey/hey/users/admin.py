from hey.users.models import User,Message

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    pass
class MessageAdmin(admin.ModelAdmin):
    pass

admin.site.register(User,UserAdmin)
admin.site.register(Message,MessageAdmin)