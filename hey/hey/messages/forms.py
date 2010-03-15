from django import forms
from django.forms.models import ModelForm

from hey.users.models import User
from hey.messages.models import TransferMessage

from django.forms.widgets import Textarea

class MessageForm(ModelForm):
    class Meta:
        model = TransferMessage
        exclude = ('sendTime')
        