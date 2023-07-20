from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Toy, Cart, UserProfile
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerProfileOrReadOnly

class ToyAPIListPagination(PageNumberPagination):
    page_size = 40
    page_query_param = page_size
    max_page_size = 10000

class ToyAPIList(generics.ListAPIView):
    queryset = Toy.objects.all()
    serializer_class = ToySerializer
    pagination_class = ToyAPIListPagination
    permission_classes = [AllowAny]
    authentication_classes = []

class FeedbackAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request: HttpRequest):
        feedbacks = Feedback.objects.filter(user=request.user)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(data=serializer.data)

    def put(self, request: HttpRequest):
        serializer = FeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'responce': 'Спасибо за обратную связь!'})

class RetrieveToyAPI(APIView):
    def get(self, request: HttpRequest, slug: str):
        toy = Toy.objects.get(slug=slug)
        serializer = ToySerializer(toy)
        return Response(data=serializer.data)
    
    def put(self, request: HttpRequest, slug: str):
        transactions = Transaction.objects.filter(user=request.user, status='RD')
        if len(transactions) > 0:
            serializer = ReviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            review = serializer.save()
            toy = Toy.objects.get(slug=slug)
            toy.reviews.add(review)
            toy.save()
            return Response({'responce': 'Спасибо за отзыв!'})
        else:
            return Response({'responce': 'Вы не можете оставить отзыв так как не приобрели товар'})
        

class TransactionAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request: HttpRequest):
        transaction = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transaction, many=True)
        return Response(data=serializer.data)
    
    def put(self, request: HttpRequest):
        cart = Cart.objects.get(user=request.user)
        new_transaction = Transaction.objects.create(user=request.user)
        for item in cart.items.all():
            new_transaction.items.add(item)
        cart.items.clear()
        new_transaction.save()
        return Response({'responce': 'Ваш заказ отправлен на обработку'})  

class CartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest):
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        #serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data)

    def put(self, request: HttpRequest):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_item = serializer.save()
        cart = Cart.objects.get(user=request.user)
        cart.items.add(cart_item)
        cart.save()
        return Response({'responce': 'Вы добавили игрушку в корзину'})


class ListToysByCategory(generics.ListAPIView):
    serializer_class = ToySerializer
    pagination_class = ToyAPIListPagination
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return Toy.objects.filter(category__slug=self.kwargs['slug'])

class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=userProfileSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)

class userProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=userProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]

class HomePage(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request: HttpRequest):
        photos = Avatar.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(data=serializer.data)







    

