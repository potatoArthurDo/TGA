from django.db import models

# Create your models here.
from django.db import models
from store.models import Product, User
# Create your models here.

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,  related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}'s wishlist item: {self.product.name}"
    