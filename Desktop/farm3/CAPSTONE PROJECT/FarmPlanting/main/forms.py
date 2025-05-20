from django import forms
from .models import UserCrop

class UserCropForm(forms.ModelForm):
    class Meta:
        model = UserCrop
        fields = ['name', 'date_planted', 'region', 'quantity', 'image']
        widgets = {
            'date_planted': forms.DateInput(attrs={'type': 'date'}),
        }
