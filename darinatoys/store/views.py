from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from .models import Toy, CartItem
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
    serializer_class = ToySerializer
    lookup_field = 'slug'
    


class ListToysByCategory(generics.ListAPIView):
    serializer_class = ToySerializer
    pagination_class = ToyAPIListPagination

    def get_queryset(self):
        return Toy.objects.filter(category__slug=self.kwargs['slug'])






    

