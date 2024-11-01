from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('checkout', views.checkout, name = 'checkout'),
    path('billing_info', views.billing_info, name = 'billing_info'),
    path('process_payment', views.process_payment, name = 'process_payment'),
    path('order_dashboard', views.order_dashboard, name = 'order_dashboard'),
    path('handle_order/<int:pk>', views.handle_order, name = 'handle_order'),
    path('order_details/<int:pk>', views.order_details, name = 'order_details'),



]