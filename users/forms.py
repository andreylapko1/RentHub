from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from users.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]




class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',required=True)
    password = forms.CharField(label='Password',required=True, widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(username=email, password=password)

        if user is None:
            raise forms.ValidationError("Invalid email or password")

        self.user_cache = user
        return self.cleaned_data

    def get_user(self):
        return self.user_cache