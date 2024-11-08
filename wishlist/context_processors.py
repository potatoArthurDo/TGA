from .models import Wishlist
from django.shortcuts import get_object_or_404

def wishlist(request):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist = wishlist.products.all()
    return {'wishlist': wishlist}