from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from restaurant.models import MenuItem, Restaurant
from restaurant.serializers import MenuItemSerializer, RestaurantSerializer

class RestaurantListAPIView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [SearchFilter]
    search_fields = ["owner__id"]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [IsAuthenticated()]


class RestaurantDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [IsAuthenticated()]


class MenuItemListAPIView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [SearchFilter]
    search_fields = ['restaurant__id']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [IsAuthenticated()]

class MenuItemDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [] 
        return [IsAuthenticated()]

