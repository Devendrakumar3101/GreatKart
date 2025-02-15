from django.shortcuts import render, HttpResponse
from .models import Product
from carts.models import Cart, CartItem
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def store(request, category_slug=None):

    if category_slug is not None:
        products = Product.objects.all().filter(category__slug = category_slug, is_available = True)
        product_count = products.count()
    
    else:
        products = Product.objects.all().filter(is_available = True)
        product_count = products.count()
    
    if request.GET.get('search'):
        products = Product.objects.all().filter(Q(product_name__icontains = request.GET.get('search')) | 
                                                Q(description__icontains = request.GET.get('search')),
                                                is_available = True
                                                )
        product_count = products.count()

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    

    context = {
        'products':page_obj,
        'product_count':product_count,
        'paginator' : paginator,
        'page_obj' : page_obj,
    }

    return render(request, 'store/store.html', context)

# def product_by_category(request, category_slug):
#     products = Product.objects.all().filter(category__slug = category_slug)

#     product_count = products.count()

#     context = {
#         'products':products,
#         'product_count':product_count,

#     }

#     return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):

    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)

    try:
        is_in_cart = CartItem.objects.filter(cart__user = request.user, product = single_product)
        # print(is_in_cart)

        # if is_in_cart:
        #     print('true')
        # else:
        #     print('false')

    except:
        is_in_cart = False

    context = {
        'single_product' : single_product,
        'is_in_cart' : is_in_cart,
    }
    return render(request, 'store/product_detail.html', context)

