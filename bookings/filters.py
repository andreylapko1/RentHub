import django_filters
from bookings.models import Booking


class BookingRangeDateFilter(django_filters.rest_framework.FilterSet):
    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte', )
    end_date = django_filters.DateFilter(field_name='end_date', lookup_expr='lte', )

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'landlord_email', 'is_confirmed',]
