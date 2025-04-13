from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
 RetrieveDestroyAPIView
from bookings.filters import BookingRangeDateFilter
from bookings.form import CreateBookingForm
from bookings.models import Booking
from bookings.serializers import BookingsListSerializer, BookingCreateSerializer, BookingToUserSerializer, \
    ConfirmCanceledBookingsSerializer
from listings.views import ListingRetrieveUpdateView
from rentapp.pagination import CustomPagination
from rentapp.permissions import IsLandlord, IsLandlordEmail, IsLandlordOrForbidden


class BookingsListView(ListAPIView):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['start_date', 'end_date', 'status', 'landlord_email',]
    ordering_fields = ['created_at', 'updated_at',]
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
    filter_backends = [ ]
    queryset = Booking.objects.all()
    serializer_class = BookingsListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delta = (instance.start_date - timezone.now()).days

        if delta >= 1:
            super().destroy(request, *args, **kwargs)
            return Response({"message": "Reservation remotely"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "You can not remove the reservation 1 days before the arrival"}, status=status.HTTP_400_BAD_REQUEST)





class BookingCreateView(CreateAPIView):
    serializer_class = BookingCreateSerializer
    queryset = Booking.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user  # Передаем пользователя в контекст
        return context


    def get(self, request, *args, **kwargs):
        if request.path.startswith('/api/'):
            serializer = BookingCreateSerializer(context=self.get_serializer_context())
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            form = CreateBookingForm(user=request.user)
            return render(request, 'bookings/booking_create.html', {'form': form})

    def create(self, request, *args, **kwargs):
        if request.path.startswith('/api/'):
            return super().create(request, *args, **kwargs)
        if request.method == 'POST':
            form = CreateBookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.renter = request.user
                booking.save()
                return redirect('booking_detail', pk=booking.pk)

    def post(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(user=request.user, data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            return Response({"id": booking.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['created_at', 'landlord_email', ]
    ordering_fields = ['created_at', 'title', 'is_confirmed']
    def get_queryset(self):
        return Booking.objects.filter(renter=self.request.user)



class UserBookingHistoryView(ListAPIView):
    pagination_class = CustomPagination
    queryset = Booking.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['created_at', 'landlord_email', ]
    ordering_fields = ['created_at', 'title', 'is_confirmed']
    serializer_class = BookingsListSerializer

    def get_queryset(self):
        return Booking.objects.filter(renter=self.request.user, end_date__lt=timezone.now(), is_confirmed=True)

# Create your views here.
