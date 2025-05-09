from django.shortcuts import render
from rest_framework import viewsets
from .models import FriedItem, Order, OrderItem, Size, Flavor
from .serializers import *

class FriedItemViewSet(viewsets.ModelViewSet):
    queryset = FriedItem.objects.all()
    serializer_class = FriedItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class FlavorViewSet(viewsets.ModelViewSet):
    queryset = Flavor.objects.all()
    serializer_class = FlavorSerializer