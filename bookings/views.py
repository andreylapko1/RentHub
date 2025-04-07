from django.utils import timezone
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
 RetrieveDestroyAPIView
from bookings.filters import BookingRangeDateFilter
from bookings.models import Booking
from bookings.serializers import BookingsListSerializer, BookingCreateSerializer, BookingToUserSerializer, \
    ConfirmCanceledBookingsSerializer
from listings.views import ListingRetrieveUpdateView
from rentapp.pagination import CustomPagination
from rentapp.permissions import IsLandlord, IsLandlordEmail, IsLandlordOrForbidden


class BookingsListView(ListAPIView):
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['start_date', 'end_date', 'status', 'landlord_email',]
    filterset_class = BookingRangeDateFilter
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer


class UserCompletedBookingsListView(ListAPIView):
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['start_date', 'end_date', 'status', 'landlord_email', ]
    filterset_class = BookingRangeDateFilter
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer


    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user, status='completed')


class BookingsDetailListView(RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delta = (instance.start_date - timezone.now()).days

        if delta >= 2:
            super().destroy(request, *args, **kwargs)
            return Response({"message": "Reservation remotely"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "You can not remove the reservation 2 days before the arrival"}, status=status.HTTP_400_BAD_REQUEST)



class BookingCreateView(CreateAPIView):
    serializer_class = BookingCreateSerializer
    queryset = Booking.objects.all()



class BookingsToUsersView(ListAPIView):
    queryset = Booking.objects.all()
    pagination_class = CustomPagination
    serializer_class = BookingToUserSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['created_at', 'is_confirmed', ]
    ordering_fields = ['created_at', 'title', 'is_confirmed']

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(landlord_email=user)


class ConfirmCanceledBookingsView(RetrieveUpdateAPIView):
    filter_backends = [ ]
    permission_classes = [IsLandlordOrForbidden]
    queryset = Booking.objects.all()
    ordering_fields = ['created_at', 'title', 'is_confirmed']
    serializer_class = ConfirmCanceledBookingsSerializer





class UserBookingsListView(ListAPIView):
    serializer_class = BookingToUserSerializer
    filterset_fields = ['created_at', 'landlord_email', ]
    ordering_fields = ['created_at', 'title', 'is_confirmed']
    def get_queryset(self):
        return Booking.objects.filter(renter=self.request.user)



class UserBookingHistoryView(ListAPIView):
    pagination_class = CustomPagination
    queryset = Booking.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['created_at', 'landlord_email', ]
    serializer_class = BookingsListSerializer

    def get_queryset(self):
        return Booking.objects.filter(renter=self.request.user, end_date__lt=timezone.now(), is_confirmed=True)

# Create your views here.
