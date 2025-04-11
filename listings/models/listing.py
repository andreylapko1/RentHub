from cities_light.models import City
from django.db import models

from rentapp import settings


class Listing(models.Model):
    TYPE_CHOICES = (
        ('home', 'Home',),
        ('apartment', 'Apartment'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    location = models.ForeignKey(City, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField()
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    landlord_email = models.CharField(max_length=255, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    views_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='listings/images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
