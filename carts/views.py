from django.shortcuts import render, HttpResponse, redirect
from store.models import Product
from django.contrib.auth import login, logout
from carts.models import Cart, CartItem
from django.shortcuts import get_object_or_404

# Create your views here.


def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user = request.user)

    else:
        # print(request.session.session_key)
        cart_items = CartItem.objects.filter(cart__session_key = request.session.session_key, cart__user = None)
        # print(cart_items)

    grand_total_price = 0
    for cart_item in cart_items:
        grand_total_price += cart_item.total_price()

    context = {
        'cart_items':cart_items,
        'grand_total_price':grand_total_price,
    }

    return render(request, 'cart/view_cart.html', context)

def add_to_cart(request, product_id):
    product = Product.objects.get(id = product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user = request.user)
        cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)

    else:
        session_key = request.session.session_key
        if session_key is None:
            request.session.create()
            session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(session_key = session_key)
        cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def remove_from_cart(request, product_id):
    product = Product.objects.get(id = product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(cart__user = request.user, product = product)

    if request.user.is_anonymous:
        cart_item = CartItem.objects.get(cart__session_key = request.session.session_key, product = product)

    cart_item.delete()

    return redirect('cart')

def increase_cart_quantity(request, product_id):
    product = Product.objects.get(id = product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(cart__user = request.user, product = product)

    if request.user.is_anonymous:
        cart_item = CartItem.objects.get(cart__session_key = request.session.session_key, product = product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

def decrease_cart_quantity(request, product_id):
    product = Product.objects.get(id = product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(cart__user = request.user, product = product)

    if request.user.is_anonymous: # else condition for above if condition
        cart_item = CartItem.objects.get(cart__session_key = request.session.session_key, product = product)

    if cart_item.quantity >= 2:
        cart_item.quantity -= 1
        cart_item.save()
    elif cart_item.quantity == 1:
        cart_item.delete()

    return redirect('cart')


    
