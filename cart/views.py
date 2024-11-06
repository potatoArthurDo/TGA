from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	# cart_products = cart.get_prods
	# quantities = cart.get_quants
	cart_items = cart.get_cart_items()
	totals = cart.cart_total()
	return render(request, "cart_summary.html", {"cart_items":cart_items, "totals":totals})




def cart_add(request):
	# Get the cart
	cart = Cart(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))
		color = request.POST.get('color', None)
		size = request.POST.get('size', None)

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)
		
		# Save to session
		cart.add(product=product, quantity=product_qty, color=color, size=size)

		# Get Cart Quantity
		cart_quantity = cart.__len__()

		# Return resonse
		# response = JsonResponse({'Product Name: ': product.name})
		response = JsonResponse({'qty': cart_quantity})
		messages.success(request, ("Product Added To Cart..."))
		return response

def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = request.POST.get('product_id')

		color = request.POST.get('color', None)
		size = request.POST.get('size', None)
		# Call delete Function in Cart
		cart.delete(product=product_id, color=color, size=size)

		response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response


def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))
		color = request.POST.get('color', None)
		size = request.POST.get('size', None)

		cart.update(product=product_id, quantity=product_qty, color=color, size=size)

		response = JsonResponse({'qty':product_qty})
		#return redirect('cart_summary')
		messages.success(request, ("Your Cart Has Been Updated..."))
		return response