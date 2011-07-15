from django.contrib import admin
from foods.models import Foods

class FoodsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Foods,FoodsAdmin)

