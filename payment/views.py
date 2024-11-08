from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import ShippingAdress, Order, OrderItem
from .forms import ShippingAdressForm, PaymentForm
from django.contrib import messages
from store.models import Profile
import datetime

# Get all user placed orders
def all_placed_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user__id = request.user.id).order_by('-date_ordered')
        return render(request, 'all_placed_orders.html', {'orders':orders})
    else:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')
def checkout(request):
    cart = Cart(request)
    # products = cart.get_prods
    # quantities = cart.get_quants
    cart_items = cart.get_cart_items()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user =  ShippingAdress.objects.get(user__id = request.user.id)
        shipping_form = ShippingAdressForm(request.POST or None, instance=shipping_user)
        return render(request, 'checkout.html', { 'cart_items':cart_items, 'totals':totals, 'shipping_form':shipping_form})
    else:
        #Not a logged in user
        shipping_form = ShippingAdressForm(request.POST or None)
        return render(request, 'checkout.html', { 'cart_items':cart_items, 'totals':totals, 'shipping_form':shipping_form})

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        # products = cart.get_prods
        # quantities = cart.get_quants
        cart_items = cart.get_cart_items()
        totals = cart.cart_total()

        #Create a session with Shipping info

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'billing_info.html', {'cart_items':cart_items, 'totals':totals, 'billing_form':billing_form, 'shipping_form' : request.POST})
        else:
            #not logged in
            billing_form = PaymentForm()
            return render(request, 'billing_info.html', {'cart_items':cart_items, 'totals':totals, 'billing_form':billing_form, 'shipping_form' : request.POST})
    
    else:
        messages.error(request, 'Acess Denined')
        return redirect('home')

def process_payment(request):
    if request.POST:
        #get the cart
        cart = Cart(request)
        products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        #get the shipping info from the last page
        payment_form = PaymentForm(request.POST or None)

        #get shipping session data
        my_shipping = request.session.get('my_shipping')

        #Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

        #Shipping Address from session
        shipping_address = f"{my_shipping['shipping_address1']}, {my_shipping['shipping_address2']}, {my_shipping['shipping_ward']}, {my_shipping['shipping_district']}, {my_shipping['shipping_city']}, {my_shipping['shipping_country']}"
        amount_paid = totals

        #CReate an Order
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            #get the order id right away
            order_id = create_order.pk

            #Add order items
            for product in products():
                product_id = product.id
                price = product.price
                for key,value in quantities().items():
                    if int(key) == product_id:
                        create_order_item = OrderItem.objects.create(order_id = order_id, user = user, product_id = product_id, quantity = value, price =price )
                        create_order_item.save()

            #Clear the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete that key
                    del request.session[key]
            
            #Get rid of the cart in the database too
            current_user = Profile.objects.filter(user__id = request.user.id)
            current_user.update(items_in_cart="")

            messages.success(request, 'Payment Completed')
            return redirect('home')
        
        else:
            # not logged in user
            #CReate order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            #get the order id right away
            order_id = create_order.pk

            #Add order items
            for product in products():
                product_id = product.id
                price = product.price
                for key,value in quantities().items():
                    if int(key) == product_id:
                        create_order_item = OrderItem.objects.create(order_id = order_id, product_id = product_id, quantity = value, price =price )
                        create_order_item.save()

            #Clear the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete that key
                    del request.session[key]
            
            messages.success(request, 'Payment Completed')
            return redirect('home')
        
def order_dashboard(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        #Get all the orders
        orders = Order.objects.all()

        return render(request, 'order_dashboard.html', {'orders': orders})
    
def handle_order(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #Get the right order
        order = Order.objects.get(id = pk)

        if request.POST:
            status = request.POST['shipping_status']
            if status == 'true':
                #Get the order
                order = Order.objects.filter(id = pk)
                #Update ordeer status
                now = datetime.datetime.now()
                order.update(shipped=True, date_delivered=now)
            else:
                #Get the order
                order = Order.objects.filter(id = pk)
                order.update(shipped=False)
            messages.success(request, 'Order Status Updated')
            return redirect('order_dashboard')
    else:
        messages.error(request, 'Access Denined')
        return redirect('home')

def order_details(request,pk):
    #Get the right order
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id = pk)
        items = OrderItem.objects.filter(order= pk)


        return render(request, 'order_details.html', {'order': order, 'items': items})
    else:
        messages.error(request, 'Access Denined')
        return redirect('home')
