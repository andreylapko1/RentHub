from cities_light.models import City
from django import forms

from listings.models import Listing


class ListingCreateForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'location' ,'price', 'rooms' ,'type' ,'image']

        location = forms.ModelChoiceField(queryset=City.objects.filter(country_id=57),
                                          empty_label="Select a city",
                                          required=True
                                          )