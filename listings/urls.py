from django.urls import path
from listings.views import ListingListView, ListingCreateView, UserListingListView, UserList, ListingRetrieveUpdateView, \
    ReviewCreateView, ListingReviewsList, ListingRetrieveView, ListingRetrieveUpdateHTMLView, ReviewCreateHTMLView

from .views import ListingListView



urlpatterns = [
    path('', ListingListView.as_view({"get": "list"}), name='listings_list'),
    path('<int:pk>/', ListingRetrieveView.as_view(), name='listing_detail'),
    path('<int:pk>/create-review', ReviewCreateHTMLView.as_view(), name='leave_review'),
    path('create/', ListingCreateView.as_view(), name='listing_create'),
    path('my/', UserListingListView.as_view(), name='listings_user_list'),
    path('userlist/', UserList.as_view(), name='userlist'),
    path('my/<int:pk>/', ListingRetrieveUpdateView.as_view(), name='my_lisings'),
    path('my/<int:pk>/update', ListingRetrieveUpdateHTMLView.as_view(), name='my_listing_update'),
    path('review/', ListingReviewsList.as_view(), name='reviews_by_listing'),
    path('review/create', ReviewCreateView.as_view(), name='review create'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)