from rest_framework import serializers
from .models import FriedItem, Order, OrderItem, Size, Flavor

class FriedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriedItem
        fields = "__all__"
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"
class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = "__all__"