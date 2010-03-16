from django import forms
from django.forms.models import ModelForm

from django.contrib.auth.models import User
from mayversion.messages.models import Message

from django.forms.widgets import Textarea


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ('sendTime','status')