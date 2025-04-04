
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from bookings.models import Booking
from bookings.serializers import BookingsListSerializer, BookingCreateSerializer, BookingToUserSerializer, \
    ConfirmCanceledBookingsSerializer
from rentapp.pagination import CustomPagination
from users.models import User


class BookingsListView(ListAPIView):
    pagination_class = CustomPagination
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer


class BookingCreateView(CreateAPIView):
    serializer_class = BookingCreateSerializer
    queryset = Booking.objects.all()


class BookingsToUsersView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = BookingToUserSerializer

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(landlord_email=user)


class ConfirmCanceledBookingsView(UpdateAPIView):
    queryset = Booking.objects.all()
    pagination_class = CustomPagination
    serializer_class = ConfirmCanceledBookingsSerializer


class UserBookingsListView(ListAPIView):
    pagination_class = CustomPagination
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# Create your views here.
