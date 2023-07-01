from rest_framework import serializers
from .models import Toy, Avatar, Cart, Category

class PhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()
    class Meta:
        model = Avatar
        fields = ['photo']

class ToySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    class Meta:
        model = Toy
        fields = ('title', 'description', 'cost', 'photos', 'category', 'slug')

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('items', )

