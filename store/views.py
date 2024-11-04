from django.shortcuts import render, redirect
from .models import Product, Profile, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, LoginForm, UpdateUserInfoForm, ChangePasswordForm
from django.db.models import Q
from payment.models import ShippingAdress
from payment.forms import ShippingAdressForm
from cart.cart import Cart
from wishlist.models import Wishlist
# Create your views here.

def user_profile(request,pk):
    
    if request.user.is_authenticated:
        user = User.objects.get(id = pk)
        return render(request, 'user_profile.html', {'user': user})
    else:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')

def search(request):
    if request.method == 'GET':
        searched = request.GET['searched_product']
        searched_product = Product.objects.filter(Q(name__contains = searched) | Q(description__contains = searched))
        if not searched_product:
            messages.error(request, 'Product does not exist')

        return render(request, 'search.html', {'searched_product': searched_product, 'searched': searched})
    else:
        return render(request, 'search.html', {})
    
def category(request, foo):
    # Replace hyphens what spaces
    foo = foo.replace('-', ' ')
    #Get the category from the url
    try:
        category = Category.objects.get(name = foo)
        products = Product.objects.filter(category = category)
        return render(request, 'category.html', {'category': category, 'products': products,})
    except:
        messages.error(request, 'Category does not exist')
        return redirect('home')
    
def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'all_categories.html', {'categories': categories})

def product(request, pk):
    product = Product.objects.get(id = pk)

    #Check if the product is in the wishlist
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        in_wishlist = wishlist.products.filter(id=product.id).exists()
    return render(request, 'product.html', {'product': product, 'in_wishlist': in_wishlist})

def change_password(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        if request.method == 'POST':
            change_password_form = ChangePasswordForm(current_user, request.POST)
            if change_password_form.is_valid():
                change_password_form.save()
                messages.success(request, 'Your password has been changed successfully')
                login(request, current_user)
                return redirect('home')
            else:
                for error in list(change_password_form.errors.values()):
                    messages.error(request, error)
                    return redirect('change_password')
        else:
            change_password_form = ChangePasswordForm(current_user)
            return render(request, 'change_password.html', {'change_password_form': change_password_form})
    else:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        update_form = UpdateUserInfoForm(request.POST or None, instance=current_user)

        #User's shipping info
        shipping_user = ShippingAdress.objects.get(user__id = request.user.id)
        #Get the shipping form too
        shipping_form = ShippingAdressForm(request.POST or None, instance=shipping_user)
        if update_form.is_valid() or shipping_form.is_valid():
            update_form.save()
            shipping_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('home')
        return render(request, 'update_info.html', {'update_form': update_form, 'shipping_form': shipping_form})
    else:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('home')
    
def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
         
            # Store email address to username field
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            #Log in immediately
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registeration successful')
            return redirect('update_info')
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information')
            return redirect('register_user')
    else:
        return render(request, 'register_user.html', {'form': form})
    
def login_user(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in')
                return redirect('home')
            else:
                print(request.POST['password']) 
                messages.error(request, 'Invalid login')
                return redirect('login_user')
        else:
            print(login_form.errors) 
            messages.error(request, 'There was an error, Please try again')
            return redirect('login_user')
    else:
        return render(request, 'login_user.html', {'login_form': login_form})
    
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {"products": products, 'categories': categories})

def about(reuqest):
    return render(reuqest, 'about.html', {})