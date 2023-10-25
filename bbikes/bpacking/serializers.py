from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['cat'] = CategorySerializer(instance.cat).data['name']
        return rep