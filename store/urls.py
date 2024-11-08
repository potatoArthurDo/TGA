from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('login_user', views.login_user, name = 'login_user'),
    path('register_user/', views.register_user, name = 'register_user'),
    path('logout_user/', views.logout_user, name = 'logout_user'),
    path('update_info', views.update_info, name = 'update_info'),
    path('change_password', views.change_password, name = 'change_password'),
    path('product/<int:pk>', views.product, name = 'product'),
    path('category/<str:foo>', views.category, name = 'category'),
    path('all_categories/', views.all_categories, name = 'all_categories'),
    path('search/', views.search, name = 'search'),
    path('user_profile/<int:pk>', views.user_profile, name = 'user_profile'),
    path('blog/', views.blog, name = 'blog'),



   
]
