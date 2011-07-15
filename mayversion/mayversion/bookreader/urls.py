from django.conf.urls.defaults import *

urlpatterns = patterns('bookreader.views',
    url(r'^workbench', 'workbench', name='book_workbench'),
    url(r'^copy_book_from_sina', 'copyBookFromSina', name='copy_book_from_sina'),
    url(r'^listbooks$', 'listBooks', name='listBooks'),
    url(r'^jsonCategories$', 'jsonCategories', name='jsonCategories'),
    url(r'^jsonbooks/(?P<category_id>\d+)$', 'jsonBooks', name='jsonBooks'),
    url(r'^book/(?P<book_id>\d+)$','bookDetails',name='bookDetails'),
)
