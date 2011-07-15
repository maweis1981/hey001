from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 6)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 6)
    address = models.CharField(max_length = 100)

    def __unicode__(self):
        return '%s - %s - %s -%s-%s' % (self.user,self.latitude,self.longitude,self.date,self.address)

