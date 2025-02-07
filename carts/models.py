from django.db import models
from accounts.models import Account
from store.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="cart", blank=True, null=True)
    session_key = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Cart of {self.user}{self.session_key}"

    def total_price(self):
        total = sum(item.total_price() for item in self.items.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} (x{self.quantity})"

    def total_price(self):
        return self.product.price * self.quantity

    sum = 0
    def grand_total_price(self):
        self.sum += self.total_price()
        return self.sum

