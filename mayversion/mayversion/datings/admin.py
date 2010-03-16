from django.contrib import admin
from datings.models import Dating

class DatingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Dating,DatingAdmin)



