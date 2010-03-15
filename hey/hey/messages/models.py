from django.db import models

from hey.users.models import User


class TransferMessage(models.Model):
    sender = models.ForeignKey(User,related_name='send_messages')
    receiver = models.ForeignKey(User,related_name='receive_messages')
    content = models.CharField(max_length=512)
    sendTime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField('isRead')
    def __unicode__(self):
        return self.receiver

    

    

