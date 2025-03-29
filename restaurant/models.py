import os
from django.db import models
from PIL import Image
from django.contrib.auth import get_user_model

User = get_user_model()

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='restaurant_image/', blank=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='restaurants', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk: 
            old_instance = Restaurant.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image.path != self.image.path:
                if os.path.isfile(old_instance.image.path):
                    os.remove(old_instance.image.path)

        super().save(*args, **kwargs)
        with Image.open(self.image.path) as img:
            target_size =300
            if img.height > target_size or img.width > target_size:
                output_size = (target_size, target_size)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def delete(self, *args, **kwargs):
        for menu_item in self.menus.all():
            if menu_item.image and os.path.isfile(menu_item.image.path):
                os.remove(menu_item.image.path)
                
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path) 
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"
    

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='menu_item_image/', blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.pk: 
            old_instance = MenuItem.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image.path != self.image.path:
                if os.path.isfile(old_instance.image.path):
                    os.remove(old_instance.image.path)

        super().save(*args, **kwargs)
        with Image.open(self.image.path) as img:
            target_size =300
            if img.height > target_size or img.width > target_size:
                output_size = (target_size, target_size)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path) 
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.restaurant.name} - {self.name} - {self.price}"