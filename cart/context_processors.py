from .cart import Cart

#Make sure cart can work on all pages
def cart(request):
    return {'cart': Cart(request)}

