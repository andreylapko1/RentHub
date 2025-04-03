from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=False) # landlord



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# Create your models here.
