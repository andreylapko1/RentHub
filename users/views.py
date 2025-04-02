from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.forms import UserRegisterForm
from users.models import User

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from users.serializers import RegisterSerializer
from users.utils import set_jwt_token


class Login(APIView):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = redirect("/api/listings")
            set_jwt_token(user, response=response)
            return response
        else:
            return render(request, "users/login.html", {"form": form})

class Logout(APIView):
    def get(self, request):
        response = redirect("/login")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

def home(request):
    return render(request, "users/home.html")


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            response = redirect("/api/listings")
            set_jwt_token(user, response=response)
            return response
        else:
            return render(request, "users/register.html", {"form": form})




# Create your views here.
