from django.shortcuts import render, HttpResponse
from .models import Product

# Create your views here.
def store(request, category_slug=None):

    if category_slug is not None:
        products = Product.objects.all().filter(category__slug = category_slug, is_available = True)
        product_count = products.count()
        
    else:
        products = Product.objects.all().filter(is_available = True)
        product_count = products.count()

    context = {
        'products':products,
        'product_count':product_count,

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
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except:
        single_product = None

    context = {
        'single_product' : single_product,
    }
    return render(request, 'store/product_detail.html', context)

