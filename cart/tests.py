from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from cart.models import Cart, CartItem
from Products.models import Product
from Users.models import UserProfile


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user, self.user)
        self.assertTrue(Cart.objects.filter(user=self.user).exists())

    def test_cart_auto_creation(self):
        new_user = User.objects.create_user(username='newuser', email='new@example.com', password='testpass123')
        cart, created = Cart.objects.get_or_create(user=new_user)
        self.assertTrue(created)
        self.assertEqual(cart.user, new_user)


class CartItemModelTest(TestCase):
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

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)

    def test_cart_item_str(self):
        # CartItem doesn't have a custom __str__ method
        self.assertIsNotNone(str(self.cart_item))


class CartDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.profile = UserProfile.objects.create(user=self.user)
        self.cart = Cart.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_cart_detail(self):
        response = self.client.get(f'/api/cart/view/{self.cart.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CartItemCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.profile = UserProfile.objects.create(user=self.user)
        self.product = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=999.99,
            quantity=10
        )
        self.client.force_authenticate(user=self.user)

    def test_add_item_to_cart(self):
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        response = self.client.post('/api/cart/item/add/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CartItem.objects.filter(product=self.product).exists())

    def test_add_item_with_nonexistent_product(self):
        data = {
            'product_id': 9999,
            'quantity': 1
        }
        response = self.client.post('/api/cart/item/add/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_same_item_increments_quantity(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        response = self.client.post('/api/cart/item/add/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 3)


class CartItemUpdateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.profile = UserProfile.objects.create(user=self.user)
        self.cart = Cart.objects.create(user=self.user)
        self.product = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=999.99,
            quantity=10
        )
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.client.force_authenticate(user=self.user)

    def test_update_cart_item_quantity(self):
        data = {'quantity': 5}
        response = self.client.put(f'/api/cart/item/update/{self.cart_item.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 5)


class CartItemDeleteViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.profile = UserProfile.objects.create(user=self.user)
        self.cart = Cart.objects.create(user=self.user)
        self.product = Product.objects.create(
            name='Laptop',
            description='High-performance laptop',
            price=999.99,
            quantity=10
        )
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.client.force_authenticate(user=self.user)

    def test_delete_cart_item(self):
        response = self.client.delete(f'/api/cart/delete/{self.cart_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(id=self.cart_item.id).exists())


class CartIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.profile = UserProfile.objects.create(user=self.user)
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
        self.client.force_authenticate(user=self.user)

    def test_full_cart_workflow(self):
        # Add first item
        data1 = {'product_id': self.product1.id, 'quantity': 1}
        response1 = self.client.post('/api/cart/item/add/', data1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Add second item
        data2 = {'product_id': self.product2.id, 'quantity': 2}
        response2 = self.client.post('/api/cart/item/add/', data2)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Update first item quantity
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product1)
        update_data = {'quantity': 3}
        response3 = self.client.put(f'/api/cart/item/update/{cart_item.id}/', update_data)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

        # Delete second item
        cart_item2 = CartItem.objects.get(cart=cart, product=self.product2)
        response4 = self.client.delete(f'/api/cart/delete/{cart_item2.id}/')
        self.assertEqual(response4.status_code, status.HTTP_204_NO_CONTENT)

        # Verify only first item remains
        self.assertEqual(CartItem.objects.filter(cart=cart).count(), 1)
