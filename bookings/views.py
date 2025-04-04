import django_filters
from django_filters import OrderingFilter, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from bookings.models import Booking
from bookings.serializers import BookingsListSerializer, BookingCreateSerializer, BookingToUserSerializer, \
    ConfirmCanceledBookingsSerializer
from rentapp.pagination import CustomPagination



class BookingsListView(ListAPIView):
    pagination_class = CustomPagination
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer


class BookingCreateView(CreateAPIView):
    serializer_class = BookingCreateSerializer
    queryset = Booking.objects.all()





class BookingsToUsersView(ListAPIView):
    queryset = Booking.objects.all()
    pagination_class = CustomPagination
    serializer_class = BookingToUserSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ['created_at', 'is_confirmed', ]
    # ordering_fields = ['created_at', 'title', 'is_confirmed'] # TODO dont work ordering

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(landlord_email=user)


class ConfirmCanceledBookingsView(UpdateAPIView):
    queryset = Booking.objects.all()
    pagination_class = CustomPagination
    serializer_class = ConfirmCanceledBookingsSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['created_at', 'start_date', 'end_date']


class UserBookingsListView(ListAPIView):
    pagination_class = CustomPagination
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# Create your views here.
