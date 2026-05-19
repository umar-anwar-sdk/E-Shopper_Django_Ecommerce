from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from home.models import Product, Category, Brand

User = get_user_model()


class HomeAPITests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            email='customer@example.com',
            password='CustomerPass123!',
            first_name='Customer',
            last_name='User'
        )
        self.vendor = User.objects.create_user(
            email='vendor@example.com',
            password='VendorPass123!',
            first_name='Vendor',
            last_name='User',
            role='vendor',
            is_verified=True,
            shop_name='Vendor Shop'
        )
        self.category = Category.objects.create(name='Electronics')
        self.brand = Brand.objects.create(name='UnitTest Brand')

    def authenticate(self, user):
        response = self.client.post('/api/auth/login/', {
            'email': user.email,
            'password': 'VendorPass123!' if user.role == 'vendor' else 'CustomerPass123!'
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['tokens']['access']}")

    def test_product_list_public(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_create_product(self):
        self.authenticate(self.customer)
        response = self.client.post('/api/create-product/', {
            'name': 'New Product',
            'details': 'Description',
            'price': 100,
            'Availability': 'In Stock',
            'Condition': 'New',
            'category_id': self.category.id,
            'brand_id': self.brand.id,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_vendor_can_create_product(self):
        self.authenticate(self.vendor)
        response = self.client.post('/api/create-product/', {
            'name': 'Vendor Product',
            'details': 'Description',
            'price': 50,
            'Availability': 'In Stock',
            'Condition': 'New',
            'category_id': self.category.id,
            'brand_id': self.brand.id,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('vendor@example.com', response.data['vendor'])

    def test_add_to_cart_requires_auth(self):
        response = self.client.post('/api/add-to-cart/', {'product_id': 999})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
