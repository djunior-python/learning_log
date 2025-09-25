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
