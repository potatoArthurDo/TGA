from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist
from store.models import Product
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def remove_from_wishlist(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=pk)

        #Get the wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        #Check if the product is already in the wishlist
        if wishlist.products.filter(id=product.id).exists():
            wishlist.products.remove(product)
            messages.success(request, 'Product removed from wishlist')
        else:
            messages.error(request, 'Product not in wishlist')
        # return redirect(reverse('product', args=[pk]))
        return redirect('wishlist')
    else:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')

def add_to_wishlist(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=pk)

        #Get or create the wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        #Check if the product is already in the wishlist
        if wishlist.products.filter(id=product.id).exists():
            messages.error(request, 'Product already in wishlist')
        else:
            wishlist.products.add(product)
            messages.success(request, 'Product added to wishlist')
        return redirect(reverse('product', args=[pk]))
    else:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')
    
def wishlist(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_items = wishlist.products.all()
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')