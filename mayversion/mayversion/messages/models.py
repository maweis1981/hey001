#!/usr/bin/env python
# encoding: utf-8


from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='send_messages')
    receiver = models.ForeignKey(User, related_name='receive_messages')
    content = models.TextField()
    sendTime = models.DateTimeField(auto_now_add = True)
    status = models.BooleanField('isRead',default=False)

    def __unicode__(self):
        return self.receiver
