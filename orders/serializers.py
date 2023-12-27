from rest_framework import serializers
from orders.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.product.name
    class Meta:
        model = OrderItem
        fields = ('product','product_name', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.total_price

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'total_price']
        read_only_fields = [ 'order_items', 'total_price']
        extra_kwargs = {
            'user': {'required': False},
        }