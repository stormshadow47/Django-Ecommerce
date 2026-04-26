from django.test import TestCase
from django.contrib.auth.models import User
from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer
from Products.models import Product


class CartItemSerializerTest(TestCase):
    """Unit tests for CartItemSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.cart = Cart.objects.create(user=self.user)
        self.product = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=999.99,
            quantity=10
        )
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
    
    def test_serialization(self):
        serializer = CartItemSerializer(self.cart_item)
        data = serializer.data
        self.assertEqual(data['quantity'], 2)
        self.assertEqual(data['product'], self.product.id)
    
    def test_deserialization_valid_data(self):
        data = {
            'cart': self.cart.id,
            'product': self.product.id,
            'quantity': 5
        }
        serializer = CartItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_deserialization_invalid_quantity(self):
        data = {
            'cart': self.cart.id,
            'product': self.product.id,
            'quantity': -1
        }
        serializer = CartItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class CartSerializerTest(TestCase):
    """Unit tests for CartSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.cart = Cart.objects.create(user=self.user)
    
    def test_serialization(self):
        serializer = CartSerializer(self.cart)
        data = serializer.data
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['items'], [])


class CartModelMethodTest(TestCase):
    """Unit tests for Cart model methods"""
    
    def test_cart_auto_creation(self):
        user = User.objects.create_user(username='newuser', email='new@example.com', password='testpass123')
        cart, created = Cart.objects.get_or_create(user=user)
        self.assertTrue(created)
        self.assertEqual(cart.user, user)
    
    def test_cart_item_creation(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        cart = Cart.objects.create(user=user)
        product = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=999.99,
            quantity=10
        )
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, product)
        self.assertEqual(cart_item.quantity, 2)
