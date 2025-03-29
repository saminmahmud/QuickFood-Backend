from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework import generics
from rest_framework.filters import SearchFilter
from order.models import Order, OrderItem
from order.serializers import OrderItemSerializer, OrderSerializer
from django.contrib.auth import get_user_model
from restaurant.models import MenuItem, Restaurant
from sslcommerz_lib import SSLCOMMERZ
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import time
import random

User = get_user_model()
STORE_ID = getattr(settings, "STORE_ID", "Unset STORE_ID in Views")
STORE_PASSWORD = getattr(settings, "STORE_PASSWORD", "Unset STORE_PASSWORD in Views")
# Views for API endpoints related to Orders

class OrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__id']

    def perform_create(self, serializer):
        order = serializer.save()
        order_data = OrderSerializer(order).data
        return Response(order_data, status=status.HTTP_201_CREATED)


class OrderListAPIViewForAdmin(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs.get('id'))
        user_restaurants = Restaurant.objects.filter(owner=user)
        return Order.objects.filter(items__restaurant__in=user_restaurants).distinct()

    def perform_create(self, serializer):
        order = serializer.save()
        order_data = OrderSerializer(order).data
        return Response(order_data, status=status.HTTP_201_CREATED)


class OrderDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemListAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filter_backends = [SearchFilter]
    search_fields = ['order__id']


class OrderItemDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


def generate_transaction_id():
    timestamp = int(time.time())
    random_num = random.randint(1000, 9999)
    return f'TX{timestamp}{random_num}'




@csrf_exempt
def Paymentview(request, order_id):
    if request.method == 'POST':
        try:
            # Parse the request body
            data = json.loads(request.body)
            items = data.get('items', [])

            # Fetch the order object
            try:
                order_qs = Order.objects.get(id=order_id, is_paid=False)
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order not found or already paid'}, status=status.HTTP_404_NOT_FOUND)

            # Create items related to the order and calculate the total price
            total_price = 0  # Initialize total price

            for item_data in items:
                try:
                    menu_item = MenuItem.objects.get(id=item_data['menu_item'])
                    restaurant = Restaurant.objects.get(id=item_data['restaurant'])
                except MenuItem.DoesNotExist:
                    return JsonResponse({'error': f"Menu item with ID {item_data['menu_item']} not found."}, status=status.HTTP_400_BAD_REQUEST)
                except Restaurant.DoesNotExist:
                    return JsonResponse({'error': f"Restaurant with ID {item_data['restaurant']} not found."}, status=status.HTTP_400_BAD_REQUEST)
                
                quantity = item_data['quantity']
                price = float(item_data['price'])  # Ensure price is a float

                # Create OrderItem
                order_item = OrderItem.objects.create(
                    order=order_qs,
                    menu_item=menu_item,
                    restaurant=restaurant,
                    quantity=quantity,
                    price=price
                )

                # Add the price to the total price of the order
                total_price += price * quantity
                total_price += 60  # Adding shipping cost, if any.

            # Update the total price and save the order
            order_qs.total_price = total_price
            order_qs.save()

            # Prepare for SSLCommerz payment
            order_total = order_qs.total_price
            tran_id = generate_transaction_id()

            store_settings = {
                'store_id': STORE_ID,  
                'store_pass': STORE_PASSWORD,
                'issandbox': True 
            }
            sslcz = SSLCOMMERZ(store_settings)
            
            post_body = {
                'total_amount': order_total,
                'currency': "BDT",
                'tran_id': tran_id,
                'success_url': f"http://localhost:8000/order/payment/purchase/{order_id}/{tran_id}/",
                'fail_url': f"http://localhost:8000/order/payment/cancle-or-fail/{order_id}/",
                'cancel_url': f"http://localhost:8000/order/payment/cancle-or-fail/{order_id}/",
                'emi_option': 0,
                'cus_name': f'{order_qs.first_name} {order_qs.last_name}',
                'cus_email': order_qs.email,
                'cus_phone': order_qs.phone,
                'cus_add1': order_qs.address,
                'cus_city': order_qs.city,
                'cus_country': "Bangladesh",
                'shipping_method': "NO",
                'num_of_item': order_qs.items.count(),
                'product_name': "Test",
                'product_category': "Test Category",
                'product_profile': "general"
            }

            # Call SSLCommerz to create a session
            response = sslcz.createSession(post_body)

            # Check if the response contains the required data
            if 'GatewayPageURL' not in response:
                return JsonResponse({'error': 'Failed to create SSLCommerz session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return JsonResponse({'redirect_url': response['GatewayPageURL']}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# View to handle the success response from the payment gateway
@csrf_exempt
def Purchase(request, order_id, tran_id):
    order_qs = Order.objects.get(id=order_id, is_paid=False)
    
    if order_qs:
        order_qs.is_paid = True
        order_qs.tran_id = tran_id
        order_qs.save()
        return HttpResponseRedirect('http://localhost:5173/my-orders?payment_status=success')

    return HttpResponseRedirect('http://localhost:5173/cart?payment_status=failed')


# View to handle the failure or cancellation of the payment
@csrf_exempt
def Cancle_or_Fail(request, order_id):
    order_qs = Order.objects.get(id=order_id, is_paid=False)
    
    if order_qs:
        order_qs.delete()
        return HttpResponseRedirect('http://localhost:5173/cart?payment_status=failed')

    return HttpResponseRedirect('http://localhost:5173/cart?payment_status=failed')
