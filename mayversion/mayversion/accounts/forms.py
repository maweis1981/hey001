from django import forms
from mayversion.accounts.models import UserProfile,UserMoreProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user')

    def save(self,user_id,commit=True):
        userProfile = super(UserProfileForm,self).save(commit=False)
        userProfile.set_user_id(user_id)
        if commit:
            userProfile.save()
        return userProfile


class UserMoreProfileForm(forms.ModelForm):
    class Meta:
        model = UserMoreProfile
        exclude = ('user')

    def save(self,user_id,commit=True):
        userMoreProfile = super(UserMoreProfileForm,self).save(commit=False)
        userMoreProfile.set_user_id(user_id)
        if commit:
            userMoreProfile.save()
        return userMoreProfile
        