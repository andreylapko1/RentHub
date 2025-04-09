from django.urls import path

from listings.views import ListingListView, ListingCreateView, UserListingListView, UserList, ListingRetrieveUpdateView, \
    ReviewCreateView, ListingViewsList, ListingRetrieveView

from rest_framework.routers import DefaultRouter
from .views import ListingListView



urlpatterns = [
    path('', ListingListView.as_view({'get': 'list'}), name='listings'),
    path('<int:pk>/', ListingRetrieveView.as_view(), name='listing_detail'),
    path('create/', ListingCreateView.as_view(), name='listings_create'),
    path('my/', UserListingListView.as_view(), name='listings_user_list'),
    path('userlist/', UserList.as_view(), name='userlist'),
    path('my/<int:pk>/', ListingRetrieveUpdateView.as_view(), name='my_lisings'),
    path('review/', ListingViewsList.as_view(), name='reviews_by_listing'),
    path('review/create', ReviewCreateView.as_view(), name='review create'),

]