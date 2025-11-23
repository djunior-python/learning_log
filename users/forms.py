from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'user_name')
        labels = {
            'user_name': 'Name',
            'email': 'Email address',
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_name']
