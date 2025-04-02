from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from users.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email',required=True)
    password = forms.CharField(label='Password',required=True)

    def clean_email(self):
        email = self.cleaned_data['username']
        try:
            get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise forms.ValidationError('Email does not exist')
        return email