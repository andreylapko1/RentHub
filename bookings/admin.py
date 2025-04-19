from django.contrib import admin
from bookings.models import Booking



@admin.register(Booking)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'renter', 'created_at', 'landlord_email')
    list_filter = ('renter', 'created_at', 'landlord_email')
    search_fields = ('title',)
    ordering = ('-created_at',)



# Register your models here.
