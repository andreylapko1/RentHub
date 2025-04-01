from django.db import models



class Listing(models.Model):
    TYPE_CHOICES = (
        ('Home', 'home',),
        ('Apartment', 'apartment'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    rooms = models.IntegerField()
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    # owner = models.ForeignKey('User', on_delete=models.CASCADE)
    # review = models.ForeignKey('Review', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
