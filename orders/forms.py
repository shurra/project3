from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    # username = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    # first_name = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    #                              max_length=32, help_text='First name')
    # last_name = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    #                             max_length=32, help_text='Last name')
    email = forms.EmailField(max_length=64, help_text='Enter a valid email address', required=True, label='e-mail',)
    # password1 = forms.CharField(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    # password2 = forms.CharField(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
