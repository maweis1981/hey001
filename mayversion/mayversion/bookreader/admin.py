from bookreader.models import Book
from django.contrib import admin

class BookAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book,BookAdmin)



