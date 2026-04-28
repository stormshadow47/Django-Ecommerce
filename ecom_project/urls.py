"""
URL configuration for ecom_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ecom_project import frontend_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontend_views.home, name='home'),
    path('products/', frontend_views.products_list, name='products'),
    path('products/<int:product_id>/', frontend_views.product_detail, name='product_detail'),
    path('cart/', frontend_views.cart_page, name='cart'),
    path('cart/count/', frontend_views.cart_count_partial, name='cart-count'),
    path('order/confirmation/<int:order_id>/', frontend_views.order_confirmation, name='order-confirmation'),
    path('login/', frontend_views.login_page, name='login'),
    path('register/', frontend_views.register_page, name='register'),
    path('logout/', frontend_views.logout_view, name='logout'),
    path('api/users/', include('Users.urls')),
    path('api/products/', include('Products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/order/', include('orders.urls')),
]
