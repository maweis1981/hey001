from django.db import models
from django.contrib.auth.models import User


class Foods(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits = 5, decimal_places=2)
    photo = models.ImageField(upload_to='foods')
    create_datetime = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s upload %s' % (self.user.username,self.name)    


    def set_user_id(self,raw_user_id):
        raw_user = User.objects.get(pk = raw_user_id)
        if raw_user:
            self.user = raw_user
        else:
            raise Exception('User not exist')