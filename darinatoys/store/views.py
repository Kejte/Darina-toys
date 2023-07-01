from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from .models import Toy, CartItem, Avatar
from .serializers import ToySerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

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

class ToyViewSet(GenericViewSet,
                 mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin):
    queryset = CartItem.objects.all()
    serializer_class = ToySerializer
    
    @action(methods=['get'], detail=True)
    def get(self, request, slug=None):
        list_photos = []
        toy = Toy.objects.get(slug=slug) 
        photos = Avatar.objects.filter(toy=toy)
        for photo in photos:
            list_photos.append(photo.photo.url)
        return Response({'title': toy.title, 'description': toy.description, 'cost': toy.cost, 'photos': list_photos, 'category': str(toy.category), 'slug': toy.slug})

    @action(methods=['put'], detail=True)
    def add_to_cart(self, request, slug=None, amount=None):
        toy = Toy.objects.get(slug=slug)
        cart_item = CartItem.objects.create(toy=toy, amount=amount)
        cart_item.save()
        return Response({'responce': 'Вы добавили игрушку в корзину'})

class ListToysByCategory(generics.ListAPIView):
    serializer_class = ToySerializer
    pagination_class = ToyAPIListPagination

    def get_queryset(self):
        return Toy.objects.filter(category__slug=self.kwargs['slug'])






    

