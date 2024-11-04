from django.contrib import admin
from .models import Product, Profile, Category, Collection

# Register your models here.
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Collection)