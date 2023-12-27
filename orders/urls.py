from django.urls import path
from orders.views import OrderCreateView, OrderHistoryView, OrderListView, OrderDetailView, OrderStatusUpdateView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('history/', OrderHistoryView.as_view(), name='order-history'),
    path('listview/', OrderListView.as_view(), name='order-list'),
    path('detailview/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('status/<int:pk>/update/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    # Other URL patterns...
]
