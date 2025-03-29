from django.urls import path
from .views import *

urlpatterns = [
    path('', OrderListAPIView.as_view(), name='order-list-create'),
    path('admin/<int:id>/', OrderListAPIViewForAdmin.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailsAPIView.as_view(), name='order-detail'),
    path('order-items/', OrderItemListAPIView.as_view(), name='order-items-list-create'),
    path('order-items/<int:pk>/', OrderItemDetailsAPIView.as_view(), name='order-items-detail'),
    path('payment/<int:order_id>/', Paymentview, name='payment-create'),
    path('payment/purchase/<int:order_id>/<tran_id>/', Purchase, name='purchase'),
    path('payment/cancle-or-fail/<int:order_id>/', Cancle_or_Fail, name='cancle-or-fail'),
]
