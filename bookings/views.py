
from rest_framework.generics import ListAPIView
from bookings.models import Booking
from bookings.serializers import BookingsListSerializer


class BookingsListView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer

# Create your views here.
