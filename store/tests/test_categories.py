from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from store.models import Category


class CategoryTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        self.admin_token = Token.objects.create(user=self.admin_user)

        self.normal_user = User.objects.create_user('normal', 'normal@example.com', 'userpass')
        self.normal_token = Token.objects.create(user=self.normal_user)

        self.category1 = Category.objects.create(name='Electronics', description='Gadgets and tech')
        self.category2 = Category.objects.create(name='Books', description='Paperbacks and hardcovers')

    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checking pagination results
        self.assertEqual(response.data['count'], 2)

    def test_retrieve_category(self):
        url = reverse('category-detail', args=[self.category1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Electronics')

    def test_create_category_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('category-list')
        data = {'name': 'Clothing', 'description': 'Shirts and pants'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)

    def test_create_category_forbidden_for_normal_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        url = reverse('category-list')
        data = {'name': 'Toys', 'description': 'Action figures'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
