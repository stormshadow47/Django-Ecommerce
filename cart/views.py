from django.shortcuts import render
from django.http import HttpRequest
from Products.models import Product
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer

class CartDetailView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the cart for the current user
        cart, created = Cart.objects.get_or_create(user=user)

        # Check if the item is already in the cart
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += int(request.data.get('quantity', 1))  # Increment quantity
            cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            # If the item is not in the cart, create a new cart item
            quantity = int(request.data.get('quantity', 1))
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemUpdateView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        quantity = int(request.data.get('quantity', instance.quantity))
        instance.quantity = quantity
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)

