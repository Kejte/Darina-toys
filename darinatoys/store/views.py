from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Toy, Cart
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework.permissions import IsAuthenticated

class ToyAPIListPagination(PageNumberPagination):
    page_size = 40
    page_query_param = page_size
    max_page_size = 10000

class ToyAPIList(generics.ListAPIView):
    queryset = Toy.objects.all()
    serializer_class = ToySerializer
    pagination_class = ToyAPIListPagination

class RetrieveToyAPI(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Toy.objects.all()
    serializer_class = ToySerializer

class TransactionAPIView(APIView):
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

    def get_queryset(self):
        return Toy.objects.filter(category__slug=self.kwargs['slug'])






    

