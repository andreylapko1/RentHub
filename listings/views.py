import django_filters
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from listings.models import Listing
from listings.permissions import IsOwner
from listings.serializers import ListingSerializer, ListingCreateSerializer, UserListSerializer, ListingUpdateSerializer
from users.models import User


class ListingKeywordFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(field_name='price')
    keyword = django_filters.CharFilter(field_name='title', method='filter_by_keywords')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    rooms = django_filters.NumberFilter(field_name='rooms')


    class Meta:
        model = Listing
        fields = ['price', 'description', 'location', 'type', 'rooms', 'keyword']

    def filter_by_keywords(self, queryset, name, value):
        return Listing.objects.filter(
            Q(description__icontains=value) | Q(title__icontains=value)
        )


class ListingListView(ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ['price', 'description', 'location', 'type', 'rooms',]
    filterset_class = ListingKeywordFilter

    def get_queryset(self):
        return Listing.objects.filter(is_active=True)






class ListingRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsOwner]
    serializer_class = ListingUpdateSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Listing.objects.filter(pk=pk)



class ListingCreateView(ListCreateAPIView):
    serializer_class = ListingCreateSerializer
    queryset = Listing.objects.all()



class UserListingListView(ListAPIView):
    serializer_class = ListingSerializer
    def get_queryset(self):
        return Listing.objects.filter(owner=self.request.user)


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer





# Create your views here.
