from django.contrib import admin
from reminds.models import UserDeviceToken,Remind,RemindLocation,RemindUserShip,RemindSendResult

class UserDeviceTokenAdmin(admin.ModelAdmin):
    pass

class RemindAdmin(admin.ModelAdmin):
    pass

class RemindLocationAdmin(admin.ModelAdmin):
    pass

class RemindUserShipAdmin(admin.ModelAdmin):
    pass

class RemindSendResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserDeviceToken,UserDeviceTokenAdmin)
admin.site.register(Remind,RemindAdmin)
admin.site.register(RemindLocation,RemindLocationAdmin)
admin.site.register(RemindUserShip,RemindUserShipAdmin)
admin.site.register(RemindSendResult,RemindSendResultAdmin)