from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from bookings.models import Booking
from listings.models import Listing


class BookingsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'




class BookingCreateSerializer(serializers.ModelSerializer):
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.none())

    class Meta:
        model = Booking
        fields = ['listing', 'start_date', 'end_date', 'status', 'renter',]
        read_only_fields = ['status', 'renter', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get('user')
        if user:
            self.fields['listing'].queryset = Listing.objects.exclude(landlord=user)


    def validate(self, data):
        listing = data['listing']
        start_date= data['start_date']
        end_date= data['end_date']

        crossing_data = Booking.objects.filter(listing=listing).filter(is_confirmed=True).filter(
            Q(start_date__lt=end_date) & Q(end_date__gt=start_date)
        )
        if crossing_data.exists():
            raise ValidationError('This listing is already registered on this date')
        return data



    # def validate(self, data):
    #     if data['start_date'] < timezone.now() or data['end_date'] < timezone.now():
    #         raise ValidationError("The start and end date should be in the future.")
    #     return data

    def create(self, validated_data):

        listing = validated_data.get('listing')
        validated_data['landlord_email'] = listing.landlord_email
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
        user = self.context['request'].user
        start_date = instance.start_date
        end_date = instance.end_date


        overlapping_bookings = Booking.objects.filter(
            landlord_email=user.email,
            is_confirmed=True,
        ).exclude(id=instance.id).filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
        )
        if overlapping_bookings.exists():
            raise ValidationError("You cannot confirm this booking because it overlaps with another confirmed booking.")


        canceled = validated_data.get('canceled', False)
        if canceled and instance.is_confirmed:
            raise ValidationError("You cannot cancel a confirmed booking.")

        if canceled:
            instance.status = 'canceled'
            instance.is_confirmed = False
        else:
            instance.is_confirmed = True
            instance.status = 'confirmed'

        instance.save()
        return instance