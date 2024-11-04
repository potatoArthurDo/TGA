from .cart import Cart

#Make sure cart can work on all pages
def cart(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    return {'cart': Cart(request), 'cart_products': cart_products}

