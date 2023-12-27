from django.urls import path
from cart.views import CartDetailView, CartItemCreateView, CartItemUpdateView, CartItemDeleteView

urlpatterns = [
    path('view/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('item/add/', CartItemCreateView.as_view(), name='cart-item-add'),
    path('item/update/<int:pk>/', CartItemUpdateView.as_view(), name='cart-item-update'),
    path('delete/<int:pk>/', CartItemDeleteView.as_view(), name='cart-item-delete'),
]