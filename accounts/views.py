from django.shortcuts import render, HttpResponse, redirect
from accounts.models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from carts.models import Cart, CartItem
from django.contrib.auth.decorators import login_required

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        # print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(password)

        nextPage = request.GET.get('next') # getting nextPage for dynamically redirect to nextPage after login. Note that this is getting using GET request.
        # print(nextPage)

        user = Account.objects.filter(email=email)

        if not user:
            messages.warning(request, "this email is not registered.")
            return redirect('loginPage')
        else:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                merge_cart(request, user)
                # login(request, user)
                
                # return redirect('home')
                if nextPage:
                    return redirect(nextPage)
                else:
                    return redirect('dashboard')
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
    messages.success(request, 'Your are successfully logged out')
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

                # Email for Activate Account
                current_site = get_current_site(request)
                subject = 'Please activate your account'
                message = render_to_string('account/account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token' : default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(subject, message, to=[to_email])
                send_email.send()

                messages.success(request, "Thankyou for registering with us. We have send a verification email to you. Please activate your account.")

                return redirect('loginPage')

    return render(request, 'account/register.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)

        user = Account.objects.filter(email = email)
        if user:
            user = Account.objects.get(email = email)
            print(user)

            # Email for Reset Password
            current_site = get_current_site(request)
            subject = "Reset Password"
            message = render_to_string('account/reset_password_email.html', {
                'user' : user,
                'domain': current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email

            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'We have send a reset password link to your email address')
            return redirect('forgotPassword')
        else:
            print("user doesn't exists")
            messages.warning(request, "Account does not exists!")
            return redirect('forgotPassword')

    return render(request, 'account/forgotPassword.html')

def resetPassword(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('reset_the_password')
    else:
        messages.warning(request, 'This link is expired')
        return redirect('loginPage')

def reset_the_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password1)
            user.save()
            messages.success(request, 'Reset password successfully.')
            return redirect('loginPage')
        else:
            messages.warning(request, 'Password are not same.')
            return render(request, 'account/resetPassword.html')
    
    return render(request, 'account/resetPassword.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Congratulations! your account is activated.')
        return redirect('loginPage')
    
    else:
        messages.warning(request, 'Invalid activation link.')
        return redirect('registerPage')

@login_required(login_url='loginPage')
def dashboard(request):
    return render(request, 'account/dashboard.html')
