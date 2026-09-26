from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from store.models import Category, Product, Order, Review


class Command(BaseCommand):
    help = 'Seeds initial sample data for Mini E-commerce REST API'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Admin & Demo User
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        admin_token, _ = Token.objects.get_or_create(user=admin_user)

        demo_user, created = User.objects.get_or_create(
            username='demouser',
            defaults={'email': 'demo@example.com'}
        )
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
        demo_token, _ = Token.objects.get_or_create(user=demo_user)

        # 2. Categories
        cat_electronics, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'description': 'Smartphones, Laptops, Accessories'}
        )
        cat_fashion, _ = Category.objects.get_or_create(
            name='Fashion',
            defaults={'description': 'Clothing, Shoes, Accessories'}
        )
        cat_books, _ = Category.objects.get_or_create(
            name='Books',
            defaults={'description': 'Fiction, Non-fiction, Tech Guides'}
        )

        # 3. Products
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'description': 'Apple flagship smartphone with titanium design and A17 Pro chip.',
                'price': 999.99,
                'stock': 20,
                'category': cat_electronics
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'description': 'Ultra smartphone with 200MP camera and S-Pen.',
                'price': 1199.99,
                'stock': 15,
                'category': cat_electronics
            },
            {
                'name': 'Sony WH-1000XM5 Headphones',
                'description': 'Industry-leading noise-canceling wireless headphones.',
                'price': 349.99,
                'stock': 30,
                'category': cat_electronics
            },
            {
                'name': 'Classic Denim Jacket',
                'description': '100% cotton casual denim jacket.',
                'price': 79.95,
                'stock': 40,
                'category': cat_fashion
            },
            {
                'name': 'Running Sneakers Pro',
                'description': 'Lightweight breathable mesh athletic shoes.',
                'price': 120.00,
                'stock': 25,
                'category': cat_fashion
            },
            {
                'name': 'Python Clean Code Design',
                'description': 'Comprehensive guide to software design principles in Python.',
                'price': 45.00,
                'stock': 50,
                'category': cat_books
            }
        ]

        products = []
        for pdata in products_data:
            p, _ = Product.objects.get_or_create(
                name=pdata['name'],
                defaults=pdata
            )
            products.append(p)

        # 4. Sample Order
        if not Order.objects.filter(user=demo_user).exists():
            prod = products[0] # iPhone 15 Pro
            qty = 1
            Order.objects.create(
                user=demo_user,
                product=prod,
                quantity=qty,
                total_price=prod.price * qty
            )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded database!\n'
            f'Admin User: admin / admin123 (Token: {admin_token.key})\n'
            f'Demo User: demouser / demo123 (Token: {demo_token.key})'
        ))
