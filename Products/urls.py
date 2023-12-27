from django.urls import path
from Products.views import ProductListView, ProductDetailView,ProductCreateView,ProductUpdateView,ProductDeleteView, ReviewList, ProductCategoryListView,ProductCategoryCreateView,ProductCategoryUpdateView,ProductCategoryDeleteView

urlpatterns = [
    path('listview/', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/reviews/', ReviewList.as_view(), name='review-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('reviews/<int:review_id>/', ReviewList.as_view(), name='review-detail'),
    path('categories/', ProductCategoryListView.as_view(), name='category-list'),
    path('categories/create/', ProductCategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', ProductCategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', ProductCategoryDeleteView.as_view(), name='category-delete'),
    # Add additional URL patterns for filtering if needed
]
