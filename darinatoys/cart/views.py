from rest_framework import generics
from store.models import Toy
from .cart import Cart
from .forms import CartAddProductForm

class CartAPI(generics.UpdateAPIView):
    pass