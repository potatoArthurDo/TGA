from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save
import datetime
from django.dispatch import receiver

# Create your models here.

class ShippingAdress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=200)
    shipping_email = models.CharField(max_length=200)
    shipping_address1 = models.CharField(max_length=200)
    shipping_address2 = models.CharField(max_length=200)
    shipping_city = models.CharField(max_length=200)
    shipping_country = models.CharField(max_length=200)
    shipping_district = models.CharField(max_length=200)
    shipping_ward = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Shipping Adresses"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
#Create a user Shipping Address by default when user is created

def create_shipping_address(sender, instance, created, **kwargs):
    if created:
        user_shipping_address = ShippingAdress(user = instance)
        user_shipping_address.save()

#Automate it
post_save.connect(create_shipping_address, sender=User)

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', "Credit Card"),
        ('vnpay', 'VNPay'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=0)
    date_ordered = models.DateTimeField(auto_now_add=True)

    date_delivered = models.DateTimeField(null=True, blank=True)
    shipped = models.BooleanField(default=False)

    #Adding payment method
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='credit_card')

    def __str__(self):
        return f'Order #{str(self.id)}'
    
#Auto add shipping date
@receiver(post_save, sender=Order)
def set_shipping_date(sender, instance, created, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        object = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not object.shipped:
            instance.date_delivered = now

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='orderitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=0)
    
    #Add color and size attributes
    color = models.CharField(max_length=15, null=True, blank=True)
    size = models.CharField(max_length=15, null=True, blank=True)
    def __str__(self):
        return f'Order Item - {str(self.id)}'