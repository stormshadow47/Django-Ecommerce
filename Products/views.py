from django.db.models import Q
from rest_framework import generics
from Products.models import Product
from Products.serializers import ProductSerializer
from Products.permissions import BuyerPermission, AdminPermission
from rest_framework.pagination import PageNumberPagination
from Users.backends import UserProfileAuthBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from Users.models import Review
from Products.models import ProductCategory
from Products.serializers import ReviewSerializer, ProductCategorySerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [BuyerPermission]
    pagination_class = PageNumberPagination  # Only authenticated users can view products

    def get_queryset(self):
        queryset = super().get_queryset()
        categories = self.request.query_params.get('categories')
        price_min = self.request.query_params.get('min_price')
        price_max = self.request.query_params.get('max_price')

        if categories:
            queryset = queryset.filter(categories=categories)
        
        # Filter by price range
        if price_min and price_max:
            queryset = queryset.filter(price__range=(price_min, price_max))
        elif price_min:
            queryset = queryset.filter(price__gte=price_min)
        elif price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset
    
    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return response

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]
    

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]
    

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]
    

class ReviewList(APIView):
    def get(self, request, product_id, format=None):
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, product_id, format=None):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product_id=product_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id, format=None):
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductCategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]
    

class ProductCategoryCreateView(generics.CreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]
    

class ProductCategoryUpdateView(generics.UpdateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]


class ProductCategoryDeleteView(generics.DestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]

