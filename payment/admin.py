from django.contrib import admin
from .models import ShippingAdress, Order, OrderItem
# Register your models here.
admin.site.register(ShippingAdress)
admin.site.register(Order)
admin.site.register(OrderItem)