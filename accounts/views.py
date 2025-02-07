from django.shortcuts import render, HttpResponse, redirect
from accounts.models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from carts.models import Cart, CartItem
from django.contrib.auth.decorators import login_required

# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        # print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(password)

        user = Account.objects.filter(email=email)

        if not user:
            messages.warning(request, "this email is not registered.")
            return redirect('loginPage')
        else:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                merge_cart(request, user)
                # login(request, user)
                
                return redirect('home')
            else:
                messages.warning(request, "Password is wrong.")
                return redirect('loginPage')

    return render(request, 'account/login.html')

def merge_cart(request, user):
    print('cart merge')

    anonymous_user_cart = {}
    anonymous_user_cart_items = [] 

    if request.session.session_key != None:
        anonymous_user_cart, created = Cart.objects.get_or_create(session_key = request.session.session_key)
        anonymous_user_cart_items = CartItem.objects.filter(cart__session_key = request.session.session_key)
        print(anonymous_user_cart_items)

    # create cart for user
    login(request, user)
    auth_user_cart, created = Cart.objects.get_or_create(user = request.user)
    auth_user_cart_items = CartItem.objects.filter(cart = auth_user_cart)

    print(request.user)

    if anonymous_user_cart_items:
        for anonymous_user_cart_item in anonymous_user_cart_items:

            increase_quantity = 0
            for auth_user_cart_item in auth_user_cart_items:
                if auth_user_cart_item.product == anonymous_user_cart_item.product:
                    increase_quantity = auth_user_cart_item.quantity

            auth_user_cart_item, created = CartItem.objects.get_or_create(cart = auth_user_cart, product = anonymous_user_cart_item.product)
            auth_user_cart_item.quantity = anonymous_user_cart_item.quantity+increase_quantity
            auth_user_cart_item.save()

            anonymous_user_cart_item.delete() #delete the cart_item of anonoymous user that is assigned to logged user
            print(f'{anonymous_user_cart_item.product.product_name} of anonymous_user_cart_items is deleted')

    if anonymous_user_cart:
        anonymous_user_cart.delete() # delete the cart of anonymous user after assign all the product to logged user
        print('anonymous_user_cart is deleted')

@login_required(login_url='loginPage')
def logoutPage(request):  
    logout(request)
    return redirect('loginPage')

def registerPage(request):
    if request.method == 'POST':
        # print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = email.split('@')[0]   # username is generate from email
        # print(username)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = Account.objects.filter(email = email)
        if user.exists():
            # print('this email is already registered')
            messages.warning(request, "this email is already registered.")
            return redirect('registerPage')
        else:
            if password1 != password2:
                messages.warning(request, "password not match.")
                return redirect('registerPage')
            else:
                user = Account.objects.create_user(first_name = first_name, last_name = last_name, email = email, username = username, password = password1)
                messages.success(request, "user is created successfully.")
                return redirect('loginPage')

    return render(request, 'account/register.html')