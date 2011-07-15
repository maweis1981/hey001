from bookreader.models import Book,Categories
from django.contrib import admin


class CategoriesAdmin(admin.ModelAdmin):
    pass

class BookAdmin(admin.ModelAdmin):
    pass


admin.site.register(Categories,CategoriesAdmin)
admin.site.register(Book,BookAdmin)



