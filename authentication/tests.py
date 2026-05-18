from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class CustomUserModelTests(TestCase):
    """Tests for CustomUser model"""
    
    def test_create_user(self):
        """Test creating a regular user"""
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
        """Test creating a superuser (admin)"""
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
        """Test customer registration API"""
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
    
    def test_login(self):
        """Test login API"""
        # Create a user first
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
        """Test login with invalid credentials"""
        data = {
            'email': 'invalid@example.com',
            'password': 'WrongPassword123!'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
