from django.shortcuts import render, HttpResponse
from store.models import Product

def home(request):
    products = Product.objects.all().filter(is_available = True)[0:4]

    new_arrived_products = Product.objects.all().filter(is_available = True).order_by('-created_date')[0:4]

    context = {
        'products':products,
        'new_arrived_products':new_arrived_products,
    }
    
    return render(request, 'home.html', context)