from django.urls import path, include
from . import views
import vnpay

urlpatterns = [

    path('payment_url/', include('vnpay.api_urls')),

]