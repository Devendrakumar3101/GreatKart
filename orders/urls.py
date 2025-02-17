from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.place_order, name='place_order'),
    path('place_order/', views.place_order, name='place_order'),
    path('make_payment/', views.make_payment, name='make_payment'),
]