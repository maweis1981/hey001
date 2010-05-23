#!/usr/bin/env python
# encoding: utf-8


from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class FriendRequest(models.Model):
    user = models.ForeignKey(User, related_name="friend_requests")
    recipientUser = models.ForeignKey(User, related_name="recipient_friend_requests")
    message = models.TextField()
    read = models.IntegerField()
    date_sent = models.DateTimeField(auto_now_add = True)
    date_read = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    #new ,accept, deny
    abuse = models.IntegerField()
    abuser_report = models.TextField()
    
    def __unicode__(self):
            return '%s add %s as friend' % self.user, self.recipientUser


class Friends(models.Model):
    user = models.ForeignKey(User, related_name="friend_master")
    friend = models.ForeignKey(User, related_name="friend_friends")
    friend_request = models.ForeignKey(FriendRequest, related_name="friend_request_approved")
    date_created = models.DateTimeField(auto_now_add=True)
    
def my_friends(user):
    friends = Friends.objects.filter(user = user)
    beFriends = Friends.objects.filter(friend = user)
    
    myFriends = friends.all() + beFriends.all()
    return myFriends    
        