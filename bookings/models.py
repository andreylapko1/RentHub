from django.db import models
from rentapp import settings


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    )
    title = models.CharField(max_length=100, null=True)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, default=1)
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    landlord_email = models.CharField(max_length=254, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.listing.title} - {self.renter}'








# Create your models here.
