from django.db import models
from rentapp import settings



class Review(models.Model):
    RATE_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey("bookings.Booking", on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(default=0, choices=RATE_CHOICES)
    review = models.TextField(null=True)
    listing = models.ForeignKey("listings.Listing", on_delete=models.CASCADE, related_name="reviews", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.booking.title}'