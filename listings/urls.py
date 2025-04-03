from django.urls import path

from listings.views import ListingListView, ListingCreateView, UserListingListView, UserList

urlpatterns = [
    path('', ListingListView.as_view(), name='bookings_list'),
    path('create/', ListingCreateView.as_view(), name='listings_list'),
    path('user/', UserListingListView.as_view(), name='listings_user_list'),
    path('userlist/', UserList.as_view(), name='userlist'),
]