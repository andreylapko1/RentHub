from django.urls import path

from listings.views import ListingListView, ListingCreateView, UserListingListView, UserList, ListingRetrieveUpdateView

urlpatterns = [
    path('', ListingListView.as_view(), name='listings'),
    path('create/', ListingCreateView.as_view(), name='listings_create'),
    path('my/', UserListingListView.as_view(), name='listings_user_list'),
    path('userlist/', UserList.as_view(), name='userlist'),
    path('my/<int:pk>/', ListingRetrieveUpdateView.as_view(), name='userlist'),
]