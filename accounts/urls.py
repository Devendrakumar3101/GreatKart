from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutPage, name='logoutPage'),
    path('register/', views.registerPage, name='registerPage'),
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('resetPassword/<uidb64>/<token>/', views.resetPassword, name='resetPassword'),
    path('reset_the_password/', views.reset_the_password, name='reset_the_password'),
] 