from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create Customer Profile
class Profile(models.Model):
    ADDRESS_CHOICES = [
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=15, blank = True)
    address1 = models.CharField(max_length=200, blank = True)
    address2 = models.CharField(max_length=200, blank = True)
    city = models.CharField(max_length=200, blank = True)
    dítrict = models.CharField(max_length=200, blank = True)
    ward = models.CharField(max_length=200, blank = True)
    country = models.CharField(max_length=200, blank = True)
    default = models.BooleanField(default = False)
    type_of_address = models.CharField(max_length=200, choices=ADDRESS_CHOICES, default='home')
    items_in_cart = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.email
    
#Create a user profile by default when user is created
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

# Create categories of Product
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

# Create product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    stock_quantiy = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Update timestamp
    is_active = models.BooleanField(default=True)  # Active status

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

# Create a collection model
class Collection(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.name
