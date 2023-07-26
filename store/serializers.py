from rest_framework import serializers
from .models import Toy, Avatar, Cart, CartItem, Transaction, Review, Feedback, UserProfile

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
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        depth = 1
        fields = ('amount', 'toy', 'total')

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        depth = 1
        fields = ('items','status')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    # total_price = serializers.SerializerMethodField()

    # def get_total_price(self, obj):
    #    return Cart().total_price()

    class Meta:
        model = Cart
        fields = ('items', 'user', 'total_price')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('toy', 'title', 'description', 'user', 'rating')

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('email', 'user', 'message', 'status')

class userProfileSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    #transactions = TransactionSerializer(many=True)
    class Meta:
        model=UserProfile
        fields='__all__'

