from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import F, Count
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from listings.filters import ListingKeywordFilter, ListingOrderingFilter
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
    filterset_fields = ['price', 'description', 'location', 'type', 'rooms',]
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
            paginator = Paginator(queryset, self.paginate_by)
            page_number = request.GET.get('page')
            listings_page = paginator.get_page(page_number)
            return render(request, 'listings/listings_list.html', {'listings': listings_page})

    def get_queryset(self):
        return Listing.objects.filter(is_active=True).annotate(review_count=Count('reviews'))

    @action(detail=False, methods=['post'], url_path='/logout') # TODO make extra_action logout button
    def logout_user(self, request):
        logout(request)
        return Response({"detail": "User logged out successfully."}, status=status.HTTP_200_OK)










class ListingRetrieveView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsLandlord]
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



class ListingCreateView(CreateAPIView):
    filter_backends = [ ]
    serializer_class = ListingCreateSerializer
    queryset = Listing.objects.all()



class UserListingListView(ListAPIView):
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ListingOrderingFilter
    ordering_fields = ['price', 'created_at', 'updated_at', 'views_count', 'review_count',]

    def get_queryset(self):
        return Listing.objects.filter(landlord=self.request.user)


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


# Create your views here.
