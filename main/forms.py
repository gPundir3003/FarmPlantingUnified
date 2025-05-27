from django import forms
from .models import UserCrop
from django.contrib.auth.models import User
from .models import Profile

class UserCropForm(forms.ModelForm):
    class Meta:
        model = UserCrop
        fields = ['name', 'date_planted', 'region', 'quantity', 'image']
        widgets = {
            'date_planted': forms.DateInput(attrs={'type': 'date'}),
        }
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']