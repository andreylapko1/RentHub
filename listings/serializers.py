from cities_light.models import City
from rest_framework import serializers

from bookings.models import Booking
from listings.models import Listing, Review
from users.models import User


class ListingSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    location = serializers.CharField(source='location.name', read_only=True)
    class Meta:
        model = Listing
        exclude = ('views_count', 'is_active', 'updated_at', 'created_at', 'landlord', )

    def get_review_count(self, obj):
        return obj.reviews.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['review_count'] = getattr(instance, 'review_count', instance.reviews.count())
        return data

class ListingViewsListSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Review
        fields = ('rate', 'review', 'created_at', 'user_email', 'listing')

class ListingDetailSerializer(serializers.ModelSerializer):
    reviews = ListingViewsListSerializer(many=True, read_only=True)
    location = serializers.CharField(source='location.name', read_only=True)
    class Meta:
        model = Listing
        fields = '__all__'


class ListingCreateSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=City.objects.filter(country=57))
    class Meta:
        model = Listing
        read_only_fields = ('landlord',)
        fields = ('title', 'description','location' ,'price','rooms', 'type','image',)


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
    location = serializers.SlugRelatedField(
        queryset=City.objects.filter(country=57),
        slug_field='name_ascii'
    )
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ('owner', 'review', 'rate', 'landlord')




class ReviewCreateSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=Review.objects.none())
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'listing',]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['booking'].queryset = Booking.objects.filter(renter=user)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        booking = validated_data['booking']

        if Review.objects.filter(booking=booking, user=user).exists():
            raise serializers.ValidationError('You have already reviewed this listing.')

        if booking.renter != user:
            raise serializers.ValidationError('You are not allowed to review listing')
        if booking.status != 'completed':
            raise serializers.ValidationError('This booking is not completed')
        validated_data['listing'] = booking.listing
        review = super().create(validated_data)
        return review





