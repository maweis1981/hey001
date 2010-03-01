from django.db import models

#survey model
class Survey(models.Model):
    title = models.CharField()
    def __unicode__(self):
        return self.title


#survey votes model
class SurveyVotes(models.Model):
    voteText = models.CharField()
    rank = models.DecimalField()
    belongSurvey = models.ManyToOneRel(Survey)
    def __unicode__(self):
        return self.voteText

