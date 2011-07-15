from django.db import models

from django.contrib.auth.models import User

REMIND_TYPES = (
    (0,'ONCE'),#remind just send push once
    (1,'TWICE'),#remind send twice push
    (2,'UNTIL'),#remind always send push until invitee mark the remind has been done.
)

REMINDS_STATUS = (
    (0,'INIT'), #remind has been create just now by creater
    (1,'INVITEE_ACCEPT'), #invitee accept the remind request
    (2,'INVITEE_DECLINE'),#invitee decline the remind request
    (3,'REMIND'),# remind successful
    (4,'REMIND_DONE'),#invitee mark the remind has been done, when remind type is "UNTIL" the remind send push notification until invitee mark remind done.
    (5,'EXPIRED'),# remind condition do not Satisfied
    (6,'CREATER_CANCELD'),#creater cancel the remind
)

TOKEN_STATUS = (
    (0,'NEW'),
    (1,'USED'),
)

class UserDeviceToken(models.Model):
    reminder = models.ForeignKey(User)
    deviceToken = models.CharField(max_length=80)
    status = models.IntegerField(choices=TOKEN_STATUS,default=0)
    register_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s-%s' % (self.reminder,self.deviceToken)


class RemindLocation(models.Model):
    creater = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 6)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 6)
    description = models.CharField(max_length = 200)
    mapImg = models.ImageField(upload_to='remind_location')
    def __unicode__(self):
        return '%s-%s-%s' % (self.creater,self.create_date,self.description)



class Remind(models.Model):
    creater = models.ForeignKey(User)
    subject = models.CharField(max_length=256)
    datetime_create = models.DateTimeField(auto_now_add=True)
    remind_type = models.IntegerField(choices = REMIND_TYPES,default=0)
    invitee = models.ManyToManyField(UserDeviceToken, through='RemindUserShip')
    location = models.ForeignKey(RemindLocation,blank=True, null=True)
    status = models.IntegerField(choices = REMINDS_STATUS,default=0)

    def __unicode__(self):
        return self.subject

class RemindUserShip(models.Model):
    user = models.ForeignKey(UserDeviceToken)
    remind = models.ForeignKey(Remind)
    date_created = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return 'Reminder[%s],Remind Creater[%s],%s' % (self.user.reminder.username,self.remind.creater.username,self.remind.subject)
    
    
class RemindSendResult(models.Model):
    remind = models.ForeignKey(Remind)
    datetime_sent = models.DateTimeField(auto_now_add=True)
