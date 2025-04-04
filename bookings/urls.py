from django.urls import path
from bookings.views import BookingsListView, BookingCreateView, BookingsToUsersView, ConfirmCanceledBookingsView

urlpatterns = [
    path('', BookingsListView.as_view(), name='bookings_list'),
    path('my/', BookingsListView.as_view(), name='bookings_list'),
    path('create/', BookingCreateView.as_view(), name='bookings_create'),
    path('applications/', BookingsToUsersView.as_view(), name='bookings_applications'),
    path('applications/<int:pk>', ConfirmCanceledBookingsView.as_view(), name='bookings_confirmation'),
]