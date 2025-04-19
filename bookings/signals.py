from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Booking

@receiver(post_save, sender=Booking)
def update_bookings_status(sender, instance, **kwargs):
    if instance.end_date < timezone.now() and instance.status != 'completed':
        instance.status = 'completed'
        instance.save()
