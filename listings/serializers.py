from rest_framework import serializers
from listings.models import Listing
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
        read_only_fields = ('owner', 'review')

