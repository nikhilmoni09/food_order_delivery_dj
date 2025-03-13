from django.db import models
from authentication.models import User
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ASSIGNED', 'Assigned'),
        ('DELIVERED', 'Delivered'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    delivery_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                     related_name='assigned_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"