from django import forms
from django.forms.models import ModelForm

from hey.users.models import User,UserMoreInfo
from django.forms.widgets import Textarea

class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ('regist_date','userMoreInfo')


class UserMoreInfoForm(ModelForm):
    class Meta:
        model = UserMoreInfo
        