from rest_framework import serializers
from bookings.models import Booking



class BookingsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
