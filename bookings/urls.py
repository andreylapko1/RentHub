from django.urls import path

from bookings.views import BookingsListView

urlpatterns = [
    path('', BookingsListView.as_view(), name='listings'),
]