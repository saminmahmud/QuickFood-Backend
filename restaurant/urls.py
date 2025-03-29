from django.urls import path
from .views import *

urlpatterns = [
    path('', RestaurantListAPIView.as_view(), name='restaurant-list-create'),
    path('<int:pk>/', RestaurantDetailsAPIView.as_view(), name='restaurant-detail'),
    path('menu/', MenuItemListAPIView.as_view(), name='menu-list-create'),
    path('menu/<int:pk>/', MenuItemDetailsAPIView.as_view(), name='menu-detail'),
]