from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Listing, Review


@receiver(post_save, sender=Review)
def update_listing_rate(sender, instance, created, **kwargs):
    if created:
        all_reviews = Review.objects.filter(listing=instance.listing)
        avg_rate = all_reviews.aggregate(Avg('rate'))['rate__avg']
        instance.listing.rate = avg_rate
        instance.listing.save()

