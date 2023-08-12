from rest_framework import serializers
from .models import Toy, Avatar, Cart, CartItem, Transaction, Review, Feedback, UserProfile

class PhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')


    class Meta:
        model = Avatar
        fields = ['image_url']

    def get_image_url(self, obj):
        return 'http://plush-toy.shop' + str(obj.photo.url)

class ToySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    overall_rating = serializers.SerializerMethodField('get_overall_rating')
    
    class Meta:
        model = Toy
        depth = 1
        fields = "__all__"

    def get_overall_rating(self, obj):
        return obj.overall_rating()

class CartItemSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        depth = 2
        fields = ('amount', 'toy', 'photos', 'total')
    
    def get_photos(self, obj):
        photos = Avatar.objects.filter(toy=obj.toy)
        serializer = PhotoSerializer(photos, many=True)
        return serializer.data

class TransactionSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Transaction
        depth = 1
        fields = ('id', 'status', 'items','total_price')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

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

