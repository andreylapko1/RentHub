from django.contrib.auth import logout
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

from listings.filters import ListingKeywordFilter, ListingOrderingFilter
from listings.models import Listing, Review
from listings.serializers import ListingSerializer, ListingCreateSerializer, UserListSerializer, \
    ListingUpdateSerializer, ReviewCreateSerializer, ListingViewsListSerializer
from rentapp.pagination import CustomPagination
from rentapp.permissions import IsLandlord
from users.models import User



class ListingListView(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['price', 'created_at', 'updated_at', 'rate']
    filterset_fields = ['price', 'description', 'location', 'type', 'rooms',]
    filterset_class = ListingKeywordFilter


    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')

    def get_queryset(self):
        return Listing.objects.filter(is_active=True)

    @action(detail=False, methods=['post'], url_path='/logout') # TODO make extra_action logout button
    def logout_user(self, request):
        logout(request)
        return Response({"detail": "User logged out successfully."}, status=status.HTTP_200_OK)




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
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = ListingOrderingFilter

    def get_queryset(self):
        return Listing.objects.filter(landlord=self.request.user)


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class ListingViewsList(ListAPIView):
    filter_backends = []
    queryset = Review.objects.all()
    serializer_class = ListingViewsListSerializer

    def get_queryset(self):
        listing_id = self.request.GET.get('listing_id')
        return Review.objects.filter(booking__listing=listing_id)

class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    filter_backends = []


# Create your views here.
