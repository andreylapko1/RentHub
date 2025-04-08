from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

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

    # def validate(self, data):
    #     if data['start_date'] < timezone.now() or data['end_date'] < timezone.now():
    #         raise ValidationError("The start and end date should be in the future.")
    #     return data

    def create(self, validated_data):
        listing = validated_data.get('listing')
        landlord_email = listing.landlord_email
        validated_data['landlord_email'] = landlord_email
        validated_data['renter'] = self.context['request'].user
        validated_data['title'] = listing.title
        return super().create(validated_data)


class BookingToUserSerializer(serializers.ModelSerializer):
    renter = serializers.CharField(source='renter.email', read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'


class ConfirmCanceledBookingsSerializer(serializers.ModelSerializer):
    canceled = serializers.BooleanField(required=False, default=False)
    is_confirmed = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['title', 'landlord_email', 'status', 'start_date', 'end_date', 'renter', 'listing', ]



    def update(self, instance, validated_data):

        if not instance:
            raise NotFound(detail="Booking with the provided ID does not exist.")

        canceled = validated_data.get('canceled', False)
        if canceled and instance.is_confirmed:
            raise ValidationError("Choose one thing")

        if canceled:
            instance.status = 'canceled'
            instance.is_confirmed = False

        else:
            instance.is_confirmed = True
            instance.status = 'confirmed'

        instance.save()
        return instance