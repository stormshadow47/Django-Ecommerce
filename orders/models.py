from django.db import models
from django.contrib.auth.models import User
from Products.models import Product
from cart.models import CartItem

class Order(models.Model):
    STATUS_CHOICES = [
        ('Order placed', 'Order placed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    items = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total_price(self):
        total = sum(item.price for item in self.order_items.all())
        self.total_price = total
        return total

    def save(self, *args, **kwargs):
        if not self.user:
            raise ValueError("User must be set before saving the Order.")
        
        if not self.pk:  # If it's a new Order being created
            super().save(*args, **kwargs)  # Save the order first to generate an ID
            
            # Rest of the logic remains the same...
        else:
            super().save(*args, **kwargs)

    @staticmethod
    def get_order_items(user):
        cart_items = CartItem.objects.filter(cart__user=user)
        return cart_items


    



class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units - ${self.price}"