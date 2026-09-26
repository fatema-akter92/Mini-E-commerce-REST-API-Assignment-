from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from store.models import Category, Product, Order


class OrderTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('alice', 'alice@example.com', 'password123')
        self.token1 = Token.objects.create(user=self.user1)

        self.user2 = User.objects.create_user('bob', 'bob@example.com', 'password123')
        self.token2 = Token.objects.create(user=self.user2)

        self.category = Category.objects.create(name='Gadgets')
        self.product = Product.objects.create(
            name='Headphones', description='Noise cancelling',
            price=150.00, stock=5, category=self.category
        )

    def test_create_order_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('order-list')
        data = {'product': self.product.id, 'quantity': 2}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['total_price']), 300.00)

        # Verify stock deduction
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_create_order_insufficient_stock(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('order-list')
        data = {'product': self.product.id, 'quantity': 10}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity', response.data)

    def test_user_can_only_view_own_orders(self):
        # Alice creates an order
        Order.objects.create(user=self.user1, product=self.product, quantity=1, total_price=150.00)

        # Bob logs in and lists orders
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        url = reverse('order-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
