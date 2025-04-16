from cities_light.models import City
from django import forms

from listings.models import Listing


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