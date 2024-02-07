from django import forms
from .models import User

class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']