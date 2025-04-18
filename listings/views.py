from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import F, Count
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.views import View
from django.views.generic import ListView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from bookings.models import Booking
from listings.filters import ListingKeywordFilter, ListingOrderingFilter
from listings.form import ListingCreateForm, UserListingsForm, ListingRetrieveUpdateForm, ReviewCreateForm
from listings.models import *
from listings.serializers import ListingSerializer, ListingCreateSerializer, UserListSerializer, \
    ListingUpdateSerializer, ReviewCreateSerializer, ListingViewsListSerializer, ListingDetailSerializer
from rentapp.pagination import CustomPagination
from rentapp.permissions import IsLandlord
from users.models import User



class ListingListView(viewsets.ModelViewSet):


    paginate_by = 6
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['price', 'created_at', 'updated_at', 'rate', 'views_count', 'review_count',]
    filterset_fields = ['price', 'location', 'type', 'rooms',]
    filterset_class = ListingKeywordFilter


    def list(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('/login')

        queryset = self.filter_queryset(self.get_queryset())

        if request.path.startswith('/api/'):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return self.get_serializer(queryset, many=True)
        else:
            query_params = request.GET.get('q', '')
            if query_params:
                queryset = queryset.filter(title__icontains=query_params) | queryset.filter(description__icontains=query_params) | queryset.filter(location__name_ascii__icontains=query_params)
            paginator = Paginator(queryset, self.paginate_by)
            page_number = request.GET.get('page')
            listings_page = paginator.get_page(page_number)
            return render(request, 'listings/listings_list.html', {'listings': listings_page})

    def get_queryset(self):
        return Listing.objects.filter(is_active=True).annotate(review_count=Count('reviews'))




class ListingRetrieveView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsLandlord, IsAuthenticated]
    serializer_class = ListingDetailSerializer
    filter_backends = []

    def get_queryset(self):
        return Listing.objects.filter(pk=self.kwargs['pk'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if request.path.startswith('/api/'):
            try:
                ListingView.objects.create(user=user, listing=instance)
                Listing.objects.filter(pk=instance.id).update(views_count=F('views_count') + 1)
            except IntegrityError:
                pass

            return super().retrieve(request, *args, **kwargs)
        else:
            return render(request, 'listings/detail_listing.html', {'listing': instance})




class ListingRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    filter_backends = []
    permission_classes = [IsLandlord]
    serializer_class = ListingUpdateSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Listing.objects.filter(pk=pk)


    def get(self, request, *args, **kwargs):
        if request.path.startswith('/api/'):
            serializer = self.get_serializer(instance=self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return render(request, 'listings/detail_listing.html', {'listing': self.get_object()})





class ListingRetrieveUpdateHTMLView(View):


    def dispatch(self, request, *args, **kwargs):
        listing = get_object_or_404(Listing, pk=kwargs['pk'])


        if listing.landlord != request.user:
            raise PermissionDenied("You do not have permission to perform this action")
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        listing = get_object_or_404(Listing, pk=kwargs['pk'])
        form = ListingRetrieveUpdateForm(instance=listing)
        return render(request, 'listings/listing_update.html', {'listing': listing, 'form': form})


    def post(self, request, *args, **kwargs):
        listing = get_object_or_404(Listing, pk=kwargs['pk'])
        form = ListingRetrieveUpdateForm(request.POST, request.FILES,instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', pk=kwargs['pk'])
        return render(request, 'listings/listing_update.html', {'form':form,'listing': listing})


    def delete(self, request, *args, **kwargs):
        listing = get_object_or_404(Listing, pk=kwargs['pk'])
        listing.delete()
        return redirect('listing_detail', pk=kwargs['pk'])




class ListingCreateView(CreateAPIView, View):
    filter_backends = [ ]
    serializer_class = ListingCreateSerializer
    queryset = Listing.objects.all()

    def get(self, request, *args, **kwargs):
        if request.path.startswith('/api/'):
            return Response({'detail': 'Method "GET" not allowed.'}, status=405)

        if not request.user.is_authenticated:
            return redirect('/login')

        form = ListingCreateForm()
        return render(request, 'listings/listing_create.html', {'form': form})

    def create(self, request, *args, **kwargs):
        if request.path.startswith('/api/'):
            return super().create(request, *args, **kwargs)

        if not request.user.is_authenticated:
            return redirect('/login')

        if request.method == 'POST':
            form = ListingCreateForm(request.POST, request.FILES)
            if form.is_valid():
                listing = form.save(commit=False)
                listing.landlord = request.user
                listing.landlord_email = request.user.email
                listing.save()
                return redirect('listing_detail', pk=listing.pk)
        else:
            form = ListingCreateForm()
        return render(request, 'listings/listing_create.html', {'form': form})



class UserListingListView(ListAPIView):
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ListingOrderingFilter
    ordering_fields = ['price', 'created_at', 'updated_at', 'views_count', 'review_count',]

    def get_queryset(self):
        return Listing.objects.filter(landlord=self.request.user)

    def get(self, request, *args, **kwargs):
        if request.path.startswith('/api/'):
            serializer = ListingSerializer(instance=self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            form = UserListingsForm(request.GET)
            return render(request, 'listings/user_listings.html', {'form': form, 'listings': self.get_queryset()})

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class ListingReviewsList(ListAPIView):
    filter_backends = []
    queryset = Review.objects.all()
    serializer_class = ListingViewsListSerializer

    def get_queryset(self):
        listing_id = self.request.GET.get('listing_id')
        return Review.objects.filter(listing=listing_id)

class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    filter_backends = []


class ReviewCreateHTMLView(View):
    queryset = Review.objects.all()

    def get(self, request, *args, **kwargs):
        # listing = Listing.objects.get(pk=kwargs['pk'])
        form = ReviewCreateForm()
        return render(request, 'listings/review_create.html', {'form': form})


    def post(self, request, *args, **kwargs):
        listing = Listing.objects.get(pk=kwargs['pk'])
        form = ReviewCreateForm(request.POST)
        print(request.POST)
        if form.is_valid():
            completed_booking = Booking.objects.filter(renter=self.request.user, listing=listing, status='completed',
                                                       is_confirmed=True)
            if completed_booking.exists():
                if Review.objects.filter(user=self.request.user, listing=listing).exists():
                    return JsonResponse({'error': 'Review already exists'}, status=status.HTTP_409_CONFLICT)
                review = form.save(commit=False)
                review.user = self.request.user
                review.booking = completed_booking.first()
                review.listing = listing
                review.save()
                return redirect('listing_detail', pk=listing.pk)
            else:
                form.add_error(None, 'You can only leave a review for completed and confirmed bookings.')

        return render(request, 'listings/review_create.html', {'form': form})







# Create your views here.
