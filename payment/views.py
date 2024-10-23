from django.shortcuts import render
from cart.cart import Cart
from .models import ShippingAdress
from .forms import ShippingAdressForm

# Create your views here.
def checkout(request):
    cart = Cart(request)
    products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user =  ShippingAdress.objects.get(user__id = request.user.id)
        shipping_form = ShippingAdressForm(request.POST or None, instance=shipping_user)
        return render(request, 'checkout.html', {'products':products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})
    else:
        #Not a logged in user
        shipping_form = ShippingAdressForm(request.POST or None)
        return render(request, 'checkout.html', {'products':products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})
