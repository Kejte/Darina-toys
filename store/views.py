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
    page_size = 20
    page_query_param = page_size
    max_page_size = 10000

class ToyAPIList(generics.ListAPIView):
    queryset = Toy.objects.filter(is_published=True)
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
        transactions = Transaction.objects.filter(user=request.user, status='RD').count()
        if int(transactions) > 0:
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
        new_transaction = Transaction.objects.create(user=request.user, total_price=cart.total_price)
        for item in cart.items.all():
            new_transaction.items.add(item)
        cart.items.update(in_cart=False)
        cart.items.clear()
        Cart.objects.filter(user=request.user).update(total_price=0)
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
        toy = Toy.objects.get(pk=request.data['toy'])
        total = toy.cost * request.data['amount']
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = Cart.objects.get(user=request.user)
        try:
            amount = CartItem.objects.get(toy=toy,cart=cart,in_cart=True).amount
            new_total = total + (CartItem.objects.get(toy=toy,cart=cart,in_cart=True).amount * CartItem.objects.get(toy=toy,cart=cart,in_cart=True).toy.cost)
            new_amount = amount + request.data['amount']
            item = CartItem.objects.filter(toy=toy, cart=cart, in_cart=True).update(amount=new_amount, total=new_total)
            cart_total_price = cart.total_price + total
            Cart.objects.filter(user=request.user).update(total_price=cart_total_price)
            return Response({'responce': 'Вы добавили товар в корзину'})
        except Exception:
            item = CartItem.objects.create(toy=toy, amount=request.data['amount'], in_cart=True, total=total)
            cart.items.add(item)
            cart_total_price = cart.total_price + total
            new_total_price = Cart.objects.filter(user=request.user).update(total_price=cart_total_price)
            return Response({'responce': 'Вы добавили товар в корзину'})
        

        
    
    def delete(self, request: HttpRequest):
        cart = Cart.objects.get(user=request.user)
        toy = Toy.objects.get(pk=request.data['toy'])
        cart_item = CartItem.objects.get(cart=cart, in_cart=True, toy=toy)
        amount_to_delete = request.data['amount']
        if cart_item.amount > amount_to_delete:
            new_amount = cart_item.amount - amount_to_delete
            new_total = new_amount * toy.cost
            new_total_price = cart.total_price - (cart_item.total - new_total)
            CartItem.objects.filter(cart=cart, in_cart=True, toy=toy).update(amount=new_amount, total=new_total)
            Cart.objects.filter(user=request.user).update(total_price=new_total_price)
            return Response({'responce': f'Из корзины было удалено {amount_to_delete} {toy.title}'})
        else:
            new_total_price = cart.total_price - cart_item.total
            cart_item.delete()
            Cart.objects.filter(user=request.user).update(total_price=new_total_price)
            return Response({'responce': f'Игрушка {toy.title} была удалена из корзины'})


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
    permission_classes=[AllowAny]
    authentication_classes = []

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)

class userProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=userProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]








    

