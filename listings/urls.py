from django.urls import path

from listings.views import ListingListView, ListingCreateView

urlpatterns = [
    path('', ListingListView.as_view(), name='bookings_list'),
    path('create/', ListingCreateView.as_view(), name='bookings_list'),
]