import django_filters
from django.db.models import Q
from listings.models import Listing


class ListingKeywordFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(field_name='price')
    keyword = django_filters.CharFilter(label='Keywords', method='filter_by_keywords')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    rooms = django_filters.NumberFilter(field_name='rooms')


    class Meta:
        model = Listing
        fields = ['price', 'description', 'location', 'type', 'rooms', 'keyword']

    def filter_by_keywords(self, queryset, name, value):
        return Listing.objects.filter(
            Q(description__icontains=value) | Q(title__icontains=value)
        )
