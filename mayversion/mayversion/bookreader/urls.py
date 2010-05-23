from django.conf.urls.defaults import *

urlpatterns = patterns('bookreader.views',
    url(r'^workbench', 'workbench', name='book_workbench'),
    url(r'^copy_book_from_sina', 'copyBookFromSina', name='copy_book_from_sina'),
    url(r'^listbooks$', 'listBooks', name='listBooks'),
)
