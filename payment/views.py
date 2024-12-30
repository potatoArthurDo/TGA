from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import ShippingAdress, Order, OrderItem
from .forms import ShippingAdressForm, PaymentForm, VNPaymentForm
from django.contrib import messages
from store.models import Profile
import datetime

#vnpay
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import random
import requests
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
# from django.utils.http import urlquote
from urllib.parse import quote as urlquote

from .vnpay import vnpay


def index(request):
    return render(request, "index.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def payment(request):

    if request.method == 'POST':
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_type = form.cleaned_data['order_type']
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount']
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']
            ipaddr = get_client_ip(request)
            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
            print(vnpay_payment_url)
            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        return render(request, "payment.html", {"title": "Thanh toán"})


def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            totalamount = True
            if totalamount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                # invalid amount
                result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            # Invalid Signature
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result


def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Thành công", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
            else:
                return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Lỗi", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
        else:
            return render(request, "payment_return.html",
                          {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                           "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                           "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
    else:
        return render(request, "payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

n = random.randint(10**11, 10**12 - 1)
n_str = str(n)
while len(n_str) < 12:
    n_str = '0' + n_str


def query(request):
    if request.method == 'GET':
        return render(request, "query.html", {"title": "Kiểm tra kết quả giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_Version = '2.1.0'

    vnp_RequestId = n_str
    vnp_Command = 'querydr'
    vnp_TxnRef = request.POST['order_id']
    vnp_OrderInfo = 'kiem tra gd'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode,
        vnp_TxnRef, vnp_TransactionDate, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "query.html", {"title": "Kiểm tra kết quả giao dịch", "response_json": response_json})

def refund(request):
    if request.method == 'GET':
        return render(request, "refund.html", {"title": "Hoàn tiền giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_RequestId = n_str
    vnp_Version = '2.1.0'
    vnp_Command = 'refund'
    vnp_TransactionType = request.POST['TransactionType']
    vnp_TxnRef = request.POST['order_id']
    vnp_Amount = request.POST['amount']
    vnp_OrderInfo = request.POST['order_desc']
    vnp_TransactionNo = '0'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_CreateBy = 'user01'
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode, vnp_TransactionType, vnp_TxnRef,
        vnp_Amount, vnp_TransactionNo, vnp_TransactionDate, vnp_CreateBy, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_Amount": vnp_Amount,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_TransactionType": vnp_TransactionType,
        "vnp_TransactionNo": vnp_TransactionNo,
        "vnp_CreateBy": vnp_CreateBy,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "refund.html", {"title": "Kết quả hoàn tiền giao dịch", "response_json": response_json})
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
        # products = cart.get_prods
        quantities = cart.get_quants
        # totals = cart.cart_total()
        cart_items = cart.get_cart_items()
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
            for item in cart_items:
                product = item['product']
                quantity = item['quantity']
                color = item['color']
                size = item['size']
                price  = product.price
                # for key,value in quantities().items():
                #     if int(key) == product_id:
                #         create_order_item = OrderItem.objects.create(order_id = order_id, user = user, product_id = product_id, quantity = value, price =price )
                #         create_order_item.save()

                create_order_item = OrderItem.objects.create(
                    order_id = order_id,
                    user = user,
                    product_id = product.id,
                    quantity = quantity,
                    color = color,
                    size = size,
                    price = price
                )
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
            for item in cart_items:
                product = item['product']
                quantity = item['quantity']
                color = item['color']
                size = item['size']
                price  = product.price
                # for key,value in quantities().items():
                #     if int(key) == product_id:
                #         create_order_item = OrderItem.objects.create(order_id = order_id, user = user, product_id = product_id, quantity = value, price =price )
                #         create_order_item.save()

                create_order_item = OrderItem.objects.create(
                    order_id = order_id,
                    product_id = product.id,
                    quantity = quantity,
                    color = color,
                    size = size,
                    price = price
                )
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
