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
    path('all_placed_orders/', views.all_placed_orders, name = 'all_placed_orders'),

    #credit card option
    path('credit_card/', views.credit_card, name= 'credit_card'),

    # #Vnpay
    path('vnpay/', views.index, name= 'index'),
    path('vnpay/payment/', views.payment, name= 'vnpay_payment'),
    path('vnpay/payment_ipn/', views.payment_ipn, name= 'vnpay_payment_ipn'),
    path('vnpay/payment_return/', views.payment_return, name= 'vnpay_payment_return'),
    path('vnpay/query/', views.query, name= 'vnpay_query'),
    path('vnpay/refund/', views.refund, name= 'vnpay_refund'),



]