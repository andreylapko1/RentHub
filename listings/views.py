from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from listings.models import Listing
from listings.serializers import ListingSerializer


class ListingListView(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = ListingSerializer




# Create your views here.
