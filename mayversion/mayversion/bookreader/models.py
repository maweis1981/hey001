from django.db import models
import settings


# Create your models here.
class Book(models.Model):
    book_id = models.CharField(max_length=50)
    book_url = models.CharField(max_length=256)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    pub_house = models.CharField(max_length=200)
    description = models.TextField()
    status = models.IntegerField()
#    cover = models.ImageField(max_length=1024, upload_to=settings.BOOKS_ROOT, blank=True)
    cover_url = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def bookFolder(self):
        return "%s/%s-%s/" % (settings.BOOKS_ROOT, self.book_id,self.title)
        
    def bookWebFolder(self):
        return "http://192.168.0.2/books/%s-%s/" % (self.book_id,self.title)

    def __unicode__(self):
        return self.title

    def toString(self):
        return "%s, %s, %s, %s" % (self.book_id, self.title,self.author,self.pub_house)
