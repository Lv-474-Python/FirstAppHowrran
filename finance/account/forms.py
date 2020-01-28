from django import forms
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    '''form for user registration'''
    username = forms.CharField(max_length=50)
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = CustomUser
        fields = ('username', 'email', 'name', 'surname', 'password', 'password2')
