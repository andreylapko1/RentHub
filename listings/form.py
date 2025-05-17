from cities_light.models import City
from django import forms

from bookings.models import Booking
from listings.models import Listing, Review


class ListingCreateForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=City.objects.filter(country_id=57),
                                      empty_label="Select a city",
                                      required=True
                                      )
    class Meta:
        model = Listing
        fields = ['title', 'description', 'location' ,'price', 'rooms' ,'type' ,'image', ]


class UserListingsForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'rooms' ,'type' ,'landlord_email']



class ListingRetrieveUpdateForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['landlord_email', 'rate', 'created_at', 'updated_at','landlord', 'views_count', ]


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rate', 'review', ]
        read_only_fields = ['user', 'listing', ]

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     listing = kwargs.pop('listing', None)
    #     super().__init__(*args, **kwargs)
    #     if user and listing:
    #         completed_booking = Booking.objects.filter(renter=user, listing=listing, status='completed', is_confirmed=True)
    #         if completed_booking.exists():
    #             pass
    #         else:
    #             self.add_error(None, 'You can only leave a review for completed and confirmed bookings.')
