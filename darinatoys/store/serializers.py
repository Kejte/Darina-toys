from rest_framework import serializers
from .models import Toy, Avatar, Cart, CartItem, Transaction, Review

class PhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()
    class Meta:
        model = Avatar
        fields = ['photo']

class ToySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    #overall_rating = Toy().overall_rating()
    class Meta:
        model = Toy
        depth = 1
        fields = ('title', 'description', 'overall_rating' , 'cost', 'photos', 'category', 'slug', 'reviews')

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
    total_price = Cart().total_price()

    class Meta:
        model = Cart
        fields = ('items', 'user', 'total_price')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('toy', 'title', 'description', 'user', 'rating')

