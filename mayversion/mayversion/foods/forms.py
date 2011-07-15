from django import forms
from foods.models import Foods

class UploadFoodForm(forms.ModelForm):
    class Meta:
        model =  Foods
        exclude = ('user','create_datetime')
        
    def save(self,user_id,commit=True):
        food = super(UploadFoodForm,self).save(commit=False)
        food.set_user_id(user_id)
        if commit:
            food.save()
        return food
    