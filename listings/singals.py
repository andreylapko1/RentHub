from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Listing, Review


@receiver(post_save, sender=Review)
def update_listing_rate(sender, instance, created, **kwargs):
    if created:
        listing = instance.booking.listing
        all_reviews = Review.objects.filter(booking__listing=listing)
        avg_rate = all_reviews.aggregate(Avg('rate'))['rate__avg']
        listing.rate = avg_rate
        listing.save()


