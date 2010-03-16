from django.db import models
from tagging.fields import TagField

# Create your models here.
from tagging.models import Tag
from django.contrib.auth.models import User

class Dating(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    creater = models.ForeignKey(User)
    city = models.CharField(max_length=30)
    status = models.IntegerField(default=1)
    type = models.IntegerField(default=1)
    start_date = models.DateField(auto_now_add=True)
    start_time = models.DateTimeField(auto_now_add=True)

    #will add more features
    dating_img = models.ImageField(max_length=1024, upload_to='/media', blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    
    tags = TagField()

    def set_tags(self,tags):
        Tag.objects.update_tags(self,tags)

    def get_tags(self,tags):
        return Tag.objects.get_for_object(self)

    def __unicode__(self):
        return self.title
