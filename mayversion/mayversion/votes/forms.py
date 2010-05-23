from django import forms
from django.forms import fields, models, formsets, widgets
from votes.models import Poll, Vote, Choice
from django.contrib.auth.models import User


class PollForm(models.ModelForm):
    class Meta:
        model = Poll
        
class ChoiceForm(models.ModelForm):
    class Meta:
        model = Choice
        exclude = ('votes',)

        
class VoteForm(models.ModelForm):
    class Meta:
        model = Vote
        
def get_polledititem_formset(form, formset=models.BaseInlineFormSet, **kwargs):
    return models.inlineformset_factory(Poll, Choice, form, formset, **kwargs)
    
def get_userpolledititem_formset(form, formset=models.BaseInlineFormSet, **kwargs):
    return models.inlineformset_factory(User, Poll, form, formset, **kwargs)
    
def get_vote_formset(form, formset=models.BaseInlineFormSet, **kwargs):
    return models.inlineformset_factory(User,Poll,Choice,form,formset,**kwargs)
    
PollFormset = formsets.formset_factory(PollForm)

ChoiceFormset = formsets.formset_factory(ChoiceForm)