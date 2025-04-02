from django.urls import path

from listings.views import ListingListView

urlpatterns = [
    path('listings/', ListingListView.as_view({'get': 'list'}), name='bookings_list'),
]