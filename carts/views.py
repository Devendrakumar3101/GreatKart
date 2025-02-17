from django.shortcuts import render, HttpResponse, redirect
from store.models import Product
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from carts.models import Cart, CartItem
from django.shortcuts import get_object_or_404

from orders.models import Order, OrderItem
import datetime
from django.contrib import messages


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

@login_required(login_url='loginPage')
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user = request.user)

    grand_total_price = 0
    for cart_item in cart_items:
        grand_total_price += cart_item.total_price()

    context = {
        'cart_items':cart_items,
        'grand_total_price':grand_total_price,
    }

    # # if PlaceOrder button click
    # if request.method == 'POST': 
    #     # print('this is a post request')
    #     first_name = request.POST.get('first_name')
    #     last_name = request.POST.get('last_name')
    #     email = request.POST.get('email')
    #     phone = request.POST.get('phone')
    #     address_line_1 = request.POST.get('address_line_1')
    #     address_line_2 = request.POST.get('address_line_2')
    #     city = request.POST.get('city')
    #     state = request.POST.get('state')
    #     country = request.POST.get('country')
    #     pincode = request.POST.get('pincode')

    #     # print(first_name, last_name, email, phone, address_line_1, address_line_2, city, state, country,  pincode )

    #     new_order = Order.objects.create(
    #         user = request.user,
    #         order_number = str(datetime.datetime.now().year) +
    #                     str(datetime.datetime.now().month) +
    #                     str(datetime.datetime.now().day) +
    #                     str(datetime.datetime.now().hour) +
    #                     str(datetime.datetime.now().minute) +
    #                     str(datetime.datetime.now().second),
            
    #         first_name = first_name,
    #         last_name = last_name,
    #         email = email,
    #         phone = phone,
    #         address_line_1 = address_line_1,
    #         address_line_2 = address_line_2,
    #         city = city,
    #         state = state,
    #         country = country,
    #         pincode = pincode,
    #         total_amount = grand_total_price,
    #         order_status = "New",
    #         payment_status = 'Pending',
    #         payment_method = 'UPI',
    #     )

    #     # for cart_item in cart_items:
    #     #     new_order_item = OrderItem.objects.create(order = new_order, product = cart_item.product, quantity = cart_item.quantity)
    #     #     cart_item.delete()

    #     # messages.success(request, "your order is received successfully, Thankyou for shopping with us")
    #     # return redirect('checkout')
    #     return render(request, 'cart/checkout.html', context)

    return render(request, 'cart/checkout.html', context)


    
