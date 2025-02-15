from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<product_id>/', views.increase_cart_quantity, name='increase_cart_quantity'),
    path('decrease/<product_id>/', views.decrease_cart_quantity, name='decrease_cart_quantity'),
    path('checkout/', views.checkout, name='checkout'),
]