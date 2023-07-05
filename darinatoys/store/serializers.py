from rest_framework import serializers
from .models import Toy, Avatar, Cart, CartItem, Transaction

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

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('amount', 'toy')

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        depth = 1
        fields = ('items','status')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('items', 'user')

