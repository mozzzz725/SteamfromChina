from django.forms import ModelForm
from .models import Game
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'password1': 'Password',
            'password2': 'Confirm Password'
        }
        help_texts = {'username': None}

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(),
        label='Remember me'
    )

    class Meta:
        fields = ['username', 'password', 'remember_me']
        labels = {
            'username': 'Username',
            'password': 'Password',
        }

from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm

class EditAccountForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the password field and help text
        self.fields.pop('password')
    class Meta:
        model = User
        fields = ['username', 'email']  # Removed password fields - they need separate handling
        labels = {
            'username': 'New Username',
            'email': 'New Email'
        }

class ChangePasswordForm(PasswordChangeForm):
    
    class Meta:
        labels = {
            'old_password': 'Current Password',
            'new_password1': 'New Password',
            'new_password2': 'Confirm New Password'
        }

class PostGameForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set empty label for genre dropdown
        self.fields['genre'].empty_label = "Select a genre"
        # Add additional HTML attributes
        self.fields['genre'].widget.attrs.update({
            'class': 'form-select',
            'aria-label': 'Game genre selection'
        })

    class Meta:
        model = Game
        fields = ['name', 'desc', 'genre', 'price', 'link']
        labels = {
            'name': 'Game Title',
            'desc': 'Description',
            'genre': 'Game Genre',
            'price': 'Price (USD)',
            'link': 'Download/Store Link'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter game title',
                'autofocus': True
            }),
            'desc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter game title',
                'autofocus': True
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/game'
            }),
        }