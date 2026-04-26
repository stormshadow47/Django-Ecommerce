"""
Smoke Tests - Quick sanity checks for critical application paths
These tests verify that the application can start and basic functionality works.
Run with: ./venv/bin/python manage.py test smoke_tests
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from Users.models import UserProfile
from Products.models import Product, ProductCategory
from cart.models import Cart, CartItem
from orders.models import Order


class SmokeTest(TestCase):
    """Basic smoke tests to verify critical paths work"""
    
    def test_database_connection(self):
        """Verify test database is accessible"""
        # This test will fail if database connection is broken
        user_count = User.objects.count()
        self.assertIsInstance(user_count, int)
    
    def test_user_model_exists(self):
        """Verify User model is accessible"""
        user = User.objects.create_user(username='smokeuser', email='smoke@example.com', password='testpass123')
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'smokeuser')
    
    def test_user_profile_creation(self):
        """Verify UserProfile can be created"""
        user = User.objects.create_user(username='smokeuser', email='smoke@example.com', password='testpass123')
        profile = UserProfile.objects.create(user=user)
        self.assertIsNotNone(profile.id)
    
    def test_product_creation(self):
        """Verify Product can be created"""
        product = Product.objects.create(
            name='Smoke Product',
            description='Test product',
            price=99.99,
            quantity=10
        )
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, 'Smoke Product')
    
    def test_product_category_creation(self):
        """Verify ProductCategory can be created"""
        category = ProductCategory.objects.create(name='Smoke Category')
        self.assertIsNotNone(category.id)
        self.assertEqual(category.name, 'Smoke Category')
    
    def test_cart_creation(self):
        """Verify Cart can be created"""
        user = User.objects.create_user(username='smokeuser', email='smoke@example.com', password='testpass123')
        cart = Cart.objects.create(user=user)
        self.assertIsNotNone(cart.id)
    
    def test_cart_item_creation(self):
        """Verify CartItem can be created"""
        user = User.objects.create_user(username='smokeuser', email='smoke@example.com', password='testpass123')
        cart = Cart.objects.create(user=user)
        product = Product.objects.create(
            name='Smoke Product',
            description='Test product',
            price=99.99,
            quantity=10
        )
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
        self.assertIsNotNone(cart_item.id)
    
    def test_order_creation(self):
        """Verify Order can be created"""
        user = User.objects.create_user(username='smokeuser', email='smoke@example.com', password='testpass123')
        order = Order.objects.create(user=user, status='Processing')
        self.assertIsNotNone(order.id)
        self.assertEqual(order.status, 'Processing')


class SmokeAPITest(TestCase):
    """Smoke tests for API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_user_registration_endpoint_exists(self):
        """Verify user registration endpoint is accessible"""
        data = {
            'username': 'smokeuser',
            'email': 'smoke@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/users/register/', data)
        # Should not return 404 or 500
        self.assertNotIn(response.status_code, [404, 500])
    
    def test_user_login_endpoint_exists(self):
        """Verify user login endpoint is accessible"""
        # First create a user
        User.objects.create_user(username='smokeuser', email='smoke@example.com', password='testpass123')
        
        data = {
            'username': 'smokeuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/users/login/', data)
        # Should not return 404 or 500
        self.assertNotIn(response.status_code, [404, 500])
    
    def test_product_list_endpoint_exists(self):
        """Verify product list endpoint is accessible"""
        response = self.client.get('/api/products/listview/')
        # Should not return 404 or 500
        self.assertNotIn(response.status_code, [404, 500])
    
    def test_category_list_endpoint_exists(self):
        """Verify category list endpoint is accessible"""
        response = self.client.get('/api/products/categories/')
        # Should not return 404 or 500
        self.assertNotIn(response.status_code, [404, 500])
    
    def test_order_history_endpoint_exists(self):
        """Verify order history endpoint is accessible"""
        user = User.objects.create_user(username='smokeuser', email='smoke@example.com', password='testpass123')
        self.client.force_authenticate(user=user)
        
        response = self.client.get('/api/order/history/')
        # Should not return 404 or 500
        self.assertNotIn(response.status_code, [404, 500])


class SmokeWorkflowTest(TestCase):
    """Smoke tests for critical user workflows"""
    
    def test_basic_user_workflow(self):
        """Test: Register → Login → Access protected endpoint"""
        client = APIClient()
        
        # Register
        register_data = {
            'username': 'smokeuser',
            'email': 'smoke@example.com',
            'password': 'testpass123'
        }
        response = client.post('/api/users/register/', register_data)
        self.assertNotIn(response.status_code, [404, 500])
        
        # Login
        login_data = {'username': 'smokeuser', 'password': 'testpass123'}
        response = client.post('/api/users/login/', login_data)
        self.assertNotIn(response.status_code, [404, 500])
        
        # Access protected endpoint
        if response.status_code == 200:
            token = response.data.get('access')
            if token:
                client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
                response = client.get('/api/order/history/')
                self.assertNotIn(response.status_code, [404, 500])
    
    def test_product_browsing_workflow(self):
        """Test: Browse products → View categories"""
        client = APIClient()
        
        # Browse products
        response = client.get('/api/products/listview/')
        self.assertNotIn(response.status_code, [404, 500])
        
        # Browse categories
        response = client.get('/api/products/categories/')
        self.assertNotIn(response.status_code, [404, 500])
