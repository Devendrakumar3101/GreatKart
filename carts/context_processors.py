from .models import Cart, CartItem
from store.models import Product

def get_total_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user = request.user)

    if request.user.is_anonymous:
        cart_items = CartItem.objects.filter(cart__session_key = request.session.session_key, cart__user = None)

    total_cart = 0

    for cart_item in cart_items:
        total_cart += cart_item.quantity

    return {
        'total_cart':total_cart
    }