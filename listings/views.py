
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from listings.filters import ListingKeywordFilter
from listings.models import Listing
from listings.permissions import IsOwner
from listings.serializers import ListingSerializer, ListingCreateSerializer, UserListSerializer, ListingUpdateSerializer
from rentapp.pagination import CustomPagination
from users.models import User



class ListingListView(ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['price', 'created_at', 'updated_at']
    filterset_fields = ['price', 'description', 'location', 'type', 'rooms',]
    filterset_class = ListingKeywordFilter

    def get_queryset(self):
        return Listing.objects.filter(is_active=True)




class ListingRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
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
        return Listing.objects.filter(landlord=self.request.user)


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer





# Create your views here.
