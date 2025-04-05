import django_filters
from django.db.models import Q
from listings.models import Listing


class ListingOrderingFilter(django_filters.rest_framework.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    created_date = django_filters.DateFilter(field_name='created_at' ,label='Created', method='filter_by_date', lookup_expr='exact')


    class Meta:
        model = Listing
        fields = ['type', 'rooms']

    def filter_by_date(self, queryset, name, value):
        value = value.strftime('%Y-%m-%d')
        return queryset.filter(created_at__date=value)



class ListingKeywordFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(label='Min price', method='filter_by_min_price')
    max_price = django_filters.NumberFilter(label='Max price', method='filter_by_max_price')
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

    def filter_by_min_price(self, queryset, name, value):
        return Listing.objects.filter(price__gte=value)

    def filter_by_max_price(self, queryset, name, value):
        return Listing.objects.filter(price__lte=value)