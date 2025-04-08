from django.contrib import admin
from listings.models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    pass
    # list_display = ('title', 'price', 'location', 'created_at')
    # list_filter = ('location', 'price')
    # search_fields = ('title', 'description')
    # ordering = ('-created_at','location')


# Register your models here.
