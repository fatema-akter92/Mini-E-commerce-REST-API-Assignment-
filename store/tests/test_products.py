from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from store.models import Category, Product


class ProductTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        self.admin_token = Token.objects.create(user=self.admin_user)

        self.category = Category.objects.create(name='Electronics', description='Tech gear')
        self.category2 = Category.objects.create(name='Fashion', description='Clothes')

        self.p1 = Product.objects.create(
            name='Smartphone iPhone', description='Latest Apple Phone',
            price=999.99, stock=10, category=self.category
        )
        self.p2 = Product.objects.create(
            name='Samsung Galaxy Phone', description='Android Flagship Phone',
            price=799.99, stock=15, category=self.category
        )
        self.p3 = Product.objects.create(
            name='Leather Jacket', description='Stylish jacket',
            price=199.99, stock=5, category=self.category2
        )

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_product_search(self):
        url = reverse('product-list') + '?search=phone'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_product_filter_by_category(self):
        url = reverse('product-list') + f'?category={self.category2.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Leather Jacket')

    def test_product_filter_by_price(self):
        url = reverse('product-list') + '?min_price=500&max_price=1000'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_product_ordering(self):
        url = reverse('product-list') + '?ordering=price'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [float(p['price']) for p in response.data['results']]
        self.assertEqual(prices, sorted(prices))

    def test_create_product_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('product-list')
        data = {
            'name': 'Laptop Dell XPS',
            'description': 'High performance laptop',
            'price': 1299.99,
            'stock': 8,
            'category': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 4)
