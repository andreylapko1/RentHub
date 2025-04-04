from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bookings.models import Booking



class BookingsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'



class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'listing',
            'start_date',
            'end_date',
            'status',
            'renter',
        ]
        read_only_fields = ['status', 'renter', 'is_confirmed']

    def validate(self, data):
        if data['start_date'] < timezone.now() or data['end_date'] < timezone.now():
            raise ValidationError("The start and end date should be in the future.")
        return data

    def create(self, validated_data):
        listing = validated_data.get('listing')
        validated_data['landlord_email'] = listing.landlord_email
        validated_data['renter'] = self.context['request'].user
        validated_data['title'] = listing.title
        return super().create(validated_data)


class BookingToUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ConfirmCanceledBookingsSerializer(serializers.ModelSerializer):
    canceled = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Booking
        fields = ['is_confirmed','canceled',]

    def update(self, instance, validated_data):
        canceled = validated_data.get('canceled', False)

        if canceled:
            instance.status = 'canceled'
            instance.is_confirmed = False
        else:
            instance.is_confirmed = True
            instance.status = 'confirmed'

        instance.save()
        return instance