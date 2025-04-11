
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from users.forms import UserRegisterForm, LoginForm

from django.contrib.auth import login
from django.shortcuts import render, redirect


from users.utils import set_jwt_token


class Login(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = redirect("/home")
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
    permission_classes = (AllowAny,)
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(data=request.POST) # TODO Dont use custom form, fix
        if form.is_valid():
            user = form.save()
            login(request, user)
            response = redirect("/home")
            set_jwt_token(user, response=response)
            return response
        else:
            return render(request, "users/register.html", {"form": form})



class ProfileView( TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context





# Create your views here.
