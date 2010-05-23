from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    owner = models.ForeignKey(User)
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.choice

class Vote(models.Model):
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User)
    choice = models.ForeignKey(Choice)
    vote_date = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return "%s choose %s for " % (self.user,self.choice,self.poll)


    