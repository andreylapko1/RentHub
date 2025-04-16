from django import forms
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from bookings.models import Booking
from listings import models
from listings.models import Listing


class CreateBookingForm(forms.ModelForm):
    listing = forms.ModelChoiceField(
        queryset=models.Listing.objects.none()
    )

    class Meta:
        model = Booking
        exclude = ('is_confirmed', 'status', 'renter', 'listings', 'landlord_email', 'title',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)
        if user:
            self.fields['listing'].queryset = Listing.objects.exclude(landlord=user)

    def clean(self, *args, **kwargs):

        cleaned_data = super().clean()
        start_date= cleaned_data['start_date']
        end_date= cleaned_data['end_date']
        listing = cleaned_data['listing']
        crossing_data = Booking.objects.filter(listing=listing).filter(is_confirmed=True).filter(
            Q(start_date__lt=end_date) & Q(end_date__gt=start_date)
        )

        if crossing_data.exists():
            raise ValidationError('This listing is already registered on this date')
        return cleaned_data


    def save(self, commit=True):
        booking = super().save(commit=False)
        listing = self.cleaned_data['listing']
        booking.landlord_email = listing.landlord.email
        if listing:
            booking.title = listing.title
        if commit:
            booking.save()
        return booking

class UserBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingDetailForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ( 'listings',)