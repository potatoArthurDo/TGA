from django.shortcuts import get_object_or_404
from .models import Wishlist

def wishlist(request):
    if request.user.is_authenticated:
        wishlist = get_object_or_404(Wishlist, user=request.user)
        wishlist_count = wishlist.products.count()
    else:
        wishlist = None  # or an empty list, depending on your needs

    return {'wishlist': wishlist, 'wishlist_count': wishlist_count}
