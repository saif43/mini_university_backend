from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import json


class AuthenticationTestCase(APITestCase):
    """Test cases for JWT Authentication API"""
    
    def setUp(self):
        """Set up test data before each test"""
        self.client = APIClient()
        self.register_url = reverse('user-register')
        self.login_url = reverse('user-login')
        self.refresh_url = reverse('token-refresh')
        self.logout_url = reverse('user-logout')
        self.profile_url = reverse('user-profile')
        self.change_password_url = reverse('change-password')
        self.status_url = reverse('auth-status')

        # Test user data
        self.test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        # Create a test user for login tests
        self.test_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpass123'
        )

    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User created successfully')
        
        # Check if user was created in database
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

    def test_user_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        # Create user first
        User.objects.create_user(username='testuser', password='pass123')
        
        response = self.client.post(self.register_url, self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_invalid_data(self):
        """Test registration with invalid data"""
        invalid_data = {
            'username': '',
            'password': '123'  # Too short
        }
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        """Test successful user login"""
        login_data = {
            'username': 'existinguser',
            'password': 'existingpass123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        invalid_login = {
            'username': 'existinguser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, invalid_login)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        """Test JWT token refresh"""
        # First login to get refresh token
        login_data = {
            'username': 'existinguser',
            'password': 'existingpass123'
        }
        login_response = self.client.post(self.login_url, login_data)
        refresh_token = login_response.data['refresh']
        
        # Test token refresh
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, refresh_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_logout_success(self):
        """Test successful logout (token blacklisting)"""
        # Login first
        login_data = {
            'username': 'existinguser',
            'password': 'existingpass123'
        }
        login_response = self.client.post(self.login_url, login_data)
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']
        
        # Logout
        logout_data = {'refresh': refresh_token}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.logout_url, logout_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_profile_access_authenticated(self):
        """Test profile access with authentication"""
        # Login and get access token
        login_data = {
            'username': 'existinguser',
            'password': 'existingpass123'
        }
        login_response = self.client.post(self.login_url, login_data)
        access_token = login_response.data['access']
        
        # Access profile with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')

    def test_profile_access_unauthenticated(self):
        """Test profile access without authentication"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_update(self):
        """Test profile update"""
        # Login and get access token
        login_data = {
            'username': 'existinguser',
            'password': 'existingpass123'
        }
        login_response = self.client.post(self.login_url, login_data)
        access_token = login_response.data['access']
        
        # Update profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        response = self.client.put(self.profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')

    def test_change_password_success(self):
        """Test successful password change"""
        # Login and get access token
        login_data = {
            'username': 'existinguser',
            'password': 'existingpass123'
        }
        login_response = self.client.post(self.login_url, login_data)
        access_token = login_response.data['access']
        
        # Change password
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        password_data = {
            'old_password': 'existingpass123',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123',
        }
        response = self.client.post(self.change_password_url, password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_wrong_old_password(self):
        """Test password change with wrong old password"""
        # Login and get access token
        login_data = {
            'username': 'existinguser',
            'password': 'existingpass123'
        }
        login_response = self.client.post(self.login_url, login_data)
        access_token = login_response.data['access']
        
        # Try to change password with wrong old password
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        password_data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123'
        }
        response = self.client.post(self.change_password_url, password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_status_authenticated(self):
        """Test authentication status check with valid token"""
        # Login and get access token
        login_data = {
            'username': 'existinguser',
            'password': 'existingpass123'
        }
        login_response = self.client.post(self.login_url, login_data)
        access_token = login_response.data['access']
        
        # Check auth status
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.status_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['authenticated'])

    def test_auth_status_unauthenticated(self):
        """Test authentication status check without token"""
        response = self.client.get(self.status_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserModelTestCase(TestCase):
    """Test cases for User model interactions"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_creation(self):
        """Test user creation"""
        user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_string_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(str(user), 'testuser')


class JWTTokenTestCase(APITestCase):
    """Test cases for JWT token functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='tokenuser',
            password='tokenpass123'
        )

    def test_token_generation(self):
        """Test JWT token generation"""
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        self.assertIsNotNone(access_token)
        self.assertIsNotNone(refresh_token)
        self.assertNotEqual(access_token, refresh_token)

    def test_token_payload(self):
        """Test JWT token payload contains user info"""
        refresh = RefreshToken.for_user(self.user)
        
        # Check if token contains user_id
        self.assertEqual(int(refresh['user_id']), self.user.id)