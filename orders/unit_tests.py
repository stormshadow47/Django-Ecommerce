from django.test import TestCase
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
from Products.models import Product


class OrderItemSerializerTest(TestCase):
    """Unit tests for OrderItemSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.order = Order.objects.create(user=self.user, status='Processing')
        self.product = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=999.99,
            quantity=10
        )
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
    
    def test_serialization(self):
        serializer = OrderItemSerializer(self.order_item)
        data = serializer.data
        self.assertEqual(data['quantity'], 2)
        self.assertEqual(data['product_name'], 'Laptop')
        self.assertEqual(float(data['price']), 1999.98)
    
    def test_product_name_method(self):
        serializer = OrderItemSerializer(self.order_item)
        self.assertEqual(serializer.get_product_name(self.order_item), 'Laptop')


class OrderSerializerTest(TestCase):
    """Unit tests for OrderSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.order = Order.objects.create(user=self.user, status='Processing')
    
    def test_serialization(self):
        serializer = OrderSerializer(self.order)
        data = serializer.data
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['order_items'], [])
    
    def test_total_price_method(self):
        serializer = OrderSerializer(self.order)
        self.assertEqual(serializer.get_total_price(self.order), self.order.total_price)


class OrderModelMethodTest(TestCase):
    """Unit tests for Order model methods"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.order = Order.objects.create(user=self.user, status='Processing')
        self.product1 = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=999.99,
            quantity=10
        )
        self.product2 = Product.objects.create(
            name='Mouse',
            description='Wireless mouse',
            price=29.99,
            quantity=50
        )
    
    def test_update_total_price(self):
        OrderItem.objects.create(order=self.order, product=self.product1, quantity=1)
        OrderItem.objects.create(order=self.order, product=self.product2, quantity=2)
        
        total = self.order.update_total_price()
        expected_total = 999.99 + (29.99 * 2)
        self.assertAlmostEqual(float(total), expected_total, places=2)
    
    def test_get_order_items(self):
        from cart.models import Cart, CartItem
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product1, quantity=1)
        
        order_items = Order.get_order_items(self.user)
        self.assertEqual(order_items.count(), 1)


class OrderItemModelMethodTest(TestCase):
    """Unit tests for OrderItem model methods"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.order = Order.objects.create(user=self.user, status='Processing')
        self.product = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=999.99,
            quantity=10
        )
    
    def test_price_calculation_on_save(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=3)
        expected_price = 999.99 * 3
        self.assertAlmostEqual(float(order_item.price), expected_price, places=2)
    
    def test_str_method(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        expected = f"{self.product.name} - 2 units - ${order_item.price}"
        self.assertEqual(str(order_item), expected)
