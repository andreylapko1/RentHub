from django.urls import path
from bookings.views import BookingsListView, BookingCreateView, BookingsToUsersView, ConfirmCanceledBookingsView, \
    BookingsDetailListView, UserBookingHistoryView, UserBookingsListView

urlpatterns = [
    path('', BookingsListView.as_view(), name='bookings_list'),
    path('my/', UserBookingsListView.as_view(), name='user_bookings'),
    path('my/completed', BookingsListView.as_view(), name='user_completed_bookings'),
    path('my/<int:pk>', BookingsDetailListView.as_view(), name='detail_booking'),
    path('create/', BookingCreateView.as_view(), name='booking_create'),
    path('applications/', BookingsToUsersView.as_view({'get': 'list'}), name='bookings_applications'),
    path('applications/<int:pk>', ConfirmCanceledBookingsView.as_view(), name='bookings_confirmation'),
    path('my/history/', UserBookingHistoryView.as_view(), name='userlist'),
]

# TODO Запретить просмотр всех бронирований (bookings list) для обычных пользователей
# TODO Завершенные бронирования
