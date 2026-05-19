from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class CustomUserModelTests(TestCase):
    """Tests for CustomUser model"""

    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'customer')
        self.assertTrue(user.is_customer())

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User'
        )
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertEqual(admin.role, 'admin')
        self.assertTrue(admin.is_admin())
        self.assertTrue(admin.is_superuser)


class AuthenticationAPITests(APITestCase):
    """Tests for authentication APIs"""

    def test_customer_registration(self):
        data = {
            'email': 'customer@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['user']['role'], 'customer')

    def test_login(self):
        User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )

        data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_invalid_login(self):
        data = {
            'email': 'invalid@example.com',
            'password': 'WrongPassword123!'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vendor_login_pending_approval(self):
        User.objects.create_user(
            email='vendor@example.com',
            password='VendorPass123!',
            first_name='Vendor',
            last_name='User',
            role='vendor',
            is_verified=False
        )

        data = {
            'email': 'vendor@example.com',
            'password': 'VendorPass123!'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('pending approval', str(response.data).lower())

    def test_admin_can_approve_vendor(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User'
        )
        vendor = User.objects.create_user(
            email='vendor@example.com',
            password='VendorPass123!',
            first_name='Vendor',
            last_name='User',
            role='vendor',
            is_verified=False
        )

        login_response = self.client.post('/api/auth/login/', {
            'email': 'admin@example.com',
            'password': 'AdminPass123!'
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['tokens']['access']

        response = self.client.patch(
            f'/api/auth/admin/vendors/{vendor.id}/approval/',
            {'approved': True},
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vendor.refresh_from_db()
        self.assertTrue(vendor.is_verified)

    def test_non_admin_cannot_list_users(self):
        user = User.objects.create_user(
            email='customer@example.com',
            password='SecurePass123!',
            first_name='Jane',
            last_name='Doe'
        )
        login_response = self.client.post('/api/auth/login/', {
            'email': 'customer@example.com',
            'password': 'SecurePass123!'
        })
        token = login_response.data['tokens']['access']

        response = self.client.get('/api/auth/admin/users/', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
