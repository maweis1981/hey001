from django import forms
from django.forms.models import ModelForm

from hey.users.models import User,UserMoreInfo
from django.forms.widgets import Textarea
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
import django.db.transaction

class UserCreationForm(forms.ModelForm):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
                                help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
                                error_message = _(
                                        "This value may contain only letters, numbers and @/./+/-/_ characters."))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
                                help_text = _("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ('username','birthday')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
                                help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
                                error_message = _(
                                        "This value may contain only letters, numbers and @/./+/-/_ characters."))

    class Meta:
        model = User

class UserForm(forms.ModelForm):
    username = forms.CharField(label=_("User Name"), max_length=30)
    gender = forms.IntegerField(label=_("Gender"),widget = forms.RadioSelect(choices =((1,'Male'),(2,'Female'))))
    email = forms.EmailField()
    birthday = forms.DateField(label=_("Birthday"),widget = SelectDateWidget(years=range(2010,1960,-1)))
    
    class Meta:
        model = User
        fields = ("username","gender","email","birthday","province","city","livecity")

    def toString(self):
        print self.cleaned_data['username']
        print self.cleaned_data['gender']
        print self.cleaned_data['email']
        print self.cleaned_data['birthday']
        print self.cleaned_data['province']
        print self.cleaned_data['city']
        print self.cleaned_data['livecity']

    def save(self,commit=True):
        user = super(UserForm,self).save(commit=False)
#        user.set_username(self.cleaned_data('username'))
#        user.set_gender(self.cleaned_data['gender'])
#        user.set_email(self.cleaned_data['email'])
#        user.set_birthday(self.cleaned_data['birthday'])
#        user.set_province(self.cleaned_data['province'])
#        user.set_city(self.cleaned_data['city'])
#        user.set_livecity(self.cleaned_data['livecity'])
        if commit:
            user.save()
        return user

class UserMoreInfoForm(forms.ModelForm):

    class Meta:
        model = UserMoreInfo
        fields = ('height','weight','blood','body','national','country',
        'gradute','industry','incoming','smoking','drinking','family','language','hobby','short')

    def save(self,user_id,commit=True):
        userMoreInfo = super(UserMoreInfoForm,self).save(commit=False)
        userMoreInfo.set_user_id(user_id)
        if commit:
            userMoreInfo.save()
        return userMoreInfo


class LoginForm(forms.Form):
    username = forms.CharField(label=_("UserName"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    
    
