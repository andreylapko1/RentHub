from rest_framework import serializers
from listings.models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('title', 'description','location' ,'price','rooms', 'type',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner_email'] = user.email
        validated_data['is_active'] = True
        return super().create(validated_data)
