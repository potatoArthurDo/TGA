from django.shortcuts import get_object_or_404
from .models import Wishlist

def wishlist(request):
    wishlist = None
    wishlist_count = 0  # Initialize to 0 for anonymous users
    if request.user.is_authenticated:
        try:
            wishlist = get_object_or_404(Wishlist, user=request.user)
            wishlist_count = wishlist.products.count()  # Count items in wishlist
        except Wishlist.DoesNotExist:
            wishlist_count = 0  # Set to 0 if no wishlist is found

    return {'wishlist_count': wishlist_count, 'wishlist': wishlist}
