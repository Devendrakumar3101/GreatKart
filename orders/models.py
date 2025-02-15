from django.db import models
from accounts.models import Account
from store.models import Product

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='orders', null=True)
    order_number = models.CharField(max_length=100, unique=True)  # Unique order identifier
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total amount of the order
    order_status = models.CharField(max_length=50, choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='New')  # Status of the order (Pending, Shipped, etc.)
    
    # Payment-related fields (optional)
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('PayPal', 'PayPal'), ('Cash on Delivery', 'Cash on Delivery'), ('UPI', 'UPI')], default='Credit Card')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Order status options
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.order_number} by {self.user}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.order.user}-{self.order.order_number}-{self.product}'




