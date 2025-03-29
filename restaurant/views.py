from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import SearchFilter

from restaurant.models import MenuItem, Restaurant
from restaurant.serializers import MenuItemSerializer, RestaurantSerializer

class RestaurantListAPIView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [SearchFilter]
    search_fields = ["owner__id"]


class RestaurantDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuItemListAPIView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [SearchFilter]
    search_fields = ['restaurant__id']

class MenuItemDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer



# from rest_framework import permissions

# class IsRestaurantOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user
# permission_classes = [IsAuthenticated, IsRestaurantOwner]
