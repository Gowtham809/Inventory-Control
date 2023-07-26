from re import template
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'), #Base URL
    path('user/', views.userPage, name='user-page'),
    path('products/', views.products, name='products'),
    path('create_product/', views.createProduct, name ='create_product'),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),

]