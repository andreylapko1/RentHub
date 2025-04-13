from dataclasses import fields

from django import forms
from bookings.models import Booking
from listings import models
from listings.models import Listing


class CreateBookingForm(forms.ModelForm):
    listings = forms.ModelChoiceField(
        queryset=models.Listing.objects.none()
    )
    class Meta:
        model = Booking
        exclude = ('is_confirmed', 'status', 'renter', 'listings', 'landlord_email')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            print("Фильтр:", user)
            self.fields['listing'].queryset = Listing.objects.exclude(landlord=user)

