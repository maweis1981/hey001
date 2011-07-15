#!/usr/bin/env python
# encoding: utf-8


from django.db import models
from django.db.models import Q
# Create your models here.
from django.contrib.auth.models import User

class FriendRequest(models.Model):
    user = models.ForeignKey(User, related_name="friend_requests")
    recipientUser = models.ForeignKey(User, related_name="recipient_friend_requests")
    message = models.TextField()
    read = models.IntegerField(default=0)
    date_sent = models.DateTimeField(auto_now_add = True)
    date_read = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(default=0)
    #new ,accept, deny
    abuse = models.IntegerField(default=0)
    abuser_report = models.TextField()
    
    def __unicode__(self):
        return '%s add %s as friend %s' % (self.user, self.recipientUser, self.message)


class Friends(models.Model):
    user = models.ForeignKey(User, related_name="friend_master")
    friend = models.ForeignKey(User, related_name="friend_friends")
    friend_request = models.ForeignKey(FriendRequest, related_name="friend_request_approved")
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s - %s - %s' % (self.user,self.friend,self.friend_request.message)
    
def all_friends_request(user):
    request_friends = FriendRequest.objects.filter(user=user)
    be_request_friends = FriendRequest.objects.filter(recipientUser=user)
    myFriendRequest = []
    for friend in request_friends:
        myFriendRequest.append(friend)
    for friend in be_request_friends:
        myFriendRequest.append(friend)
    return myFriendRequest

def my_friends_request(user):
    request_friends = FriendRequest.objects.filter(user=user)
    be_request_friends = FriendRequest.objects.filter(recipientUser=user)
    myFriendRequest = []
    for friend in request_friends:
        myFriendRequest.append(friend)
    for friend in be_request_friends:
        myFriendRequest.append(friend)
    return myFriendRequest
        

def my_friends(user):
    friends = Friends.objects.filter(Q(user = user) | Q(friend = user))
    return friends
        