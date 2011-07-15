from django.db import models

from django.contrib.auth.models import User

WEIBO_STATUS = (
    (0,'VALID'),
    (1,'INVALID'),
)

class WeiboAccessToken(models.Model):
    user = models.ForeignKey(User)
    screen_name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    statu = models.IntegerField(WEIBO_STATUS,default=0)
    
    def __unicode__(self):
        return '%s,%s' % (self.user.username,self.screen_name)