from django.utils import timezone
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
 RetrieveDestroyAPIView
from bookings.models import Booking
from bookings.serializers import BookingsListSerializer, BookingCreateSerializer, BookingToUserSerializer, \
    ConfirmCanceledBookingsSerializer
from rentapp.pagination import CustomPagination



class BookingsListView(ListAPIView):
    pagination_class = CustomPagination
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer

class BookingsDetailListView(RetrieveDestroyAPIView):
    pagination_class = CustomPagination
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
    filter_backends = (DjangoFilterBackend, )
    # ordering_fields = ['created_at', 'start_date', 'end_date']  # TODO dont work ordering


class UserBookingsListView(ListAPIView):
    pagination_class = CustomPagination
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# Create your views here.
