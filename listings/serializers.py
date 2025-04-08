from rest_framework import serializers

from bookings.models import Booking
from listings.models import Listing, Review
from users.models import User


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        read_only_fields = ('landlord',)
        fields = ('title', 'description','location' ,'price','rooms', 'type',)

    def create(self, validated_data):
        user = self.context['request'].user
        user.is_owner = True
        user.save()
        validated_data['landlord_email'] = user.email
        validated_data['landlord'] = user
        validated_data['is_active'] = True
        return super().create(validated_data)

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ListingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ('owner', 'review', 'rate', 'landlord')


class ListingViewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rate', 'review', 'created_at', )

class ReviewCreateSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=Review.objects.none())
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['booking'].queryset = Booking.objects.filter(renter=user)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        booking = validated_data['booking']

        if Review.objects.filter(booking=booking, user=user).exists():
            raise serializers.ValidationError('You have already reviewed this booking.')

        if booking.renter != user:
            raise serializers.ValidationError('You are not allowed to review bookings')
        if booking.status != 'completed':
            raise serializers.ValidationError('This booking is not completed')
        review = super().create(validated_data)
        return review





