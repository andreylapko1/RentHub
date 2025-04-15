from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
 RetrieveDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from bookings.filters import BookingRangeDateFilter
from bookings.form import CreateBookingForm, UserBookingForm
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
    # renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    # def get(self, request, *args, **kwargs):
    #     if request.accepted_renderer.format == 'html':
    #         form = CreateBookingForm(user=request.user)
    #         return render(request, 'bookings/booking_create.html', {'form': form})
    #     else:
    #         print('AAAAAAAAAA')
    #         serializer = BookingCreateSerializer(context=self.get_serializer_context())
    #         return Response(serializer.data, status=status.HTTP_200_OK)


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
        else:
            print("POST Data:", request.POST)
            form = CreateBookingForm(request.POST, user=self.request.user)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.renter = request.user
                booking.save()
                return redirect('/bookings/my')
            else:
                return render(request, 'bookings/booking_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if request.path.startswith('/api/'):
            serializer = BookingCreateSerializer(context=self.get_serializer_context(), data=request.data)
            if serializer.is_valid():
                booking = serializer.save()
                return Response({"id": booking.id}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            super().post(request, *args, **kwargs)
            return redirect('/bookings/my')






class BookingsToUsersView(ModelViewSet):
    paginate_by = 6
    queryset = Booking.objects.all()
    pagination_class = CustomPagination
    serializer_class = BookingToUserSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['created_at', 'is_confirmed', ]
    ordering_fields = ['created_at', 'title', 'is_confirmed']

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(landlord_email=user)


    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')

        queryset = self.filter_queryset(self.get_queryset())

        if request.path.startswith('/api/'):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(queryset, many=True)
                return self.get_paginated_response(serializer.data)
            return self.get_serializer(queryset, many=True)
        else:
            paginator = Paginator(queryset, self.paginate_by)
            page = request.GET.get('page')
            bookings = paginator.get_page(page)
            return render(request, 'bookings/bookings_list.html', {'bookings': bookings})


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


    def get(self, request, *args, **kwargs):
        if request.path.startswith('/api/'):
            serializer = BookingToUserSerializer(instance=self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            form = UserBookingForm(request.GET)
            return render(request, 'bookings/user_bookings.html', {'form': form, 'bookings': self.get_queryset()})



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
