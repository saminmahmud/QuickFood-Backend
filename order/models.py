from django.db import models
from restaurant.models import MenuItem, Restaurant
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    ORDER_STATUS = (
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    tran_id = models.CharField(max_length=100, null=True, blank= True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Preparing')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.is_paid}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, related_name='order_items', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='order_restaurant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.id} - {self.menu_item.name} - {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity