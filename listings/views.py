from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from listings.models import Listing
from listings.serializers import ListingSerializer, ListingCreateSerializer, UserListSerializer
from users.models import User


class ListingListView(ListAPIView):
    queryset = Listing.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = ListingSerializer



class ListingCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = ListingCreateSerializer
    queryset = Listing.objects.all()

class UserListingListView(ListView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = ListingSerializer

    def get_queryset(self):
        return Listing.objects.filter(owner=self.request.user)


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)




# Create your views here.
