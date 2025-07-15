from .models import Wishlist

def wishlist(request):
    wishlist = None
    wishlist_count = 0  # Initialize to 0 for anonymous users

    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_count = wishlist.products.count()
        except Wishlist.DoesNotExist:
            wishlist = None
            wishlist_count = 0

    return {'wishlist_count': wishlist_count, 'wishlist': wishlist}
