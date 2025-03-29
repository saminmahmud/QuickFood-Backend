from rest_framework import serializers

from order.models import Order, OrderItem
from restaurant.serializers import MenuItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city', 'status', 'tran_id', 'total_price', 'created_at', 'is_paid', 'items']
    
    def get_total_price(self, obj):
        return obj.get_total_cost()