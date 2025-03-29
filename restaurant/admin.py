from django.contrib import admin

from restaurant.models import MenuItem, Restaurant

admin.site.register(Restaurant)
admin.site.register(MenuItem)

