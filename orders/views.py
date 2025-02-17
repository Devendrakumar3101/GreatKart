from django.shortcuts import render, redirect, HttpResponse
from carts.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
import datetime

# Create your views here.
@login_required(login_url='loginPage')
def place_order(request):
    cart_items = CartItem.objects.filter(cart__user = request.user)

    grand_total_price = 0
    for cart_item in cart_items:
        grand_total_price += cart_item.total_price()

    
    
    # if PlaceOrder button click
    if request.method == 'POST': 
        # print('this is a post request')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')

        # print(first_name, last_name, email, phone, address_line_1, address_line_2, city, state, country,  pincode )

        new_order_number = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)

        new_order = Order.objects.create(
            user = request.user,
            order_number = new_order_number,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            address_line_1 = address_line_1,
            address_line_2 = address_line_2,
            city = city,
            state = state,
            country = country,
            pincode = pincode,
            total_amount = grand_total_price,
            order_status = "New",
            payment_status = 'Pending',
            payment_method = 'UPI',
        )

        order_details = Order.objects.get(order_number = new_order_number)

        context = {
        'cart_items':cart_items,
        'grand_total_price':grand_total_price,
        'order_details': order_details,

        }

        # for cart_item in cart_items:
        #     new_order_item = OrderItem.objects.create(order = new_order, product = cart_item.product, quantity = cart_item.quantity)
        #     cart_item.delete()

        # messages.success(request, "your order is received successfully, Thankyou for shopping with us")
        # return redirect('checkout')
        return render(request, 'order/place_order.html', context)
    
    context = {
        'cart_items':cart_items,
        'grand_total_price':grand_total_price,
    }

    return render(request, 'order/place_order.html', context)

def make_payment(request):
    cart_items = CartItem.objects.filter(cart__user = request.user)

    new_order = Order.objects.filter(user = request.user).order_by('-created_at')
    # print(new_order) #this is a queryset and their zero index represent latest order

    for cart_item in cart_items:
        new_order_item = OrderItem.objects.create(order = new_order[0], product = cart_item.product, quantity = cart_item.quantity)
        cart_item.delete()

    messages.success(request, f"Your Order is received. We have sent an email on your email address. \n Thank You for shopping with us.")
    return render(request, 'order/order_confirmed.html')

