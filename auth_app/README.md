# Authentication App - JWT Token API Documentation

## Overview
The `auth_app` provides JWT-based authentication for the Mini University backend project. It includes user registration, login, logout, profile management, and password change functionality.

## Features
- ✅ User Registration
- ✅ JWT Token-based Authentication (Login)
- ✅ Token Refresh
- ✅ User Logout (Token Blacklisting)
- ✅ User Profile Management
- ✅ Password Change
- ✅ Authentication Status Check
- ✅ Swagger Documentation

## API Endpoints

### Authentication Endpoints

#### 1. User Registration
- **URL**: `POST /api/auth/register/`
- **Description**: Register a new user
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string",
    "password_confirm": "string"
  }
  ```
- **Response**: User created successfully with user ID

#### 2. User Login
- **URL**: `POST /api/auth/login/`
- **Description**: Login user and receive JWT tokens
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**: 
  ```json
  {
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token",
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "first_name": "Test",
      "last_name": "User"
    }
  }
  ```

#### 3. Token Refresh
- **URL**: `POST /api/auth/token/refresh/`
- **Description**: Refresh access token using refresh token
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "refresh": "jwt_refresh_token"
  }
  ```
- **Response**: New access token

#### 4. User Logout
- **URL**: `POST /api/auth/logout/`
- **Description**: Logout user by blacklisting refresh token
- **Authentication**: Required (Bearer token)
- **Request Body**:
  ```json
  {
    "refresh": "jwt_refresh_token"
  }
  ```

### User Management Endpoints

#### 5. User Profile
- **GET URL**: `GET /api/auth/profile/`
- **PATCH URL**: `PATCH /api/auth/profile/`
- **Description**: Get or update user profile
- **Authentication**: Required (Bearer token)

#### 6. Change Password
- **URL**: `POST /api/auth/change-password/`
- **Description**: Change user password
- **Authentication**: Required (Bearer token)
- **Request Body**:
  ```json
  {
    "old_password": "string",
    "new_password": "string",
    "confirm_password": "string"
  }
  ```

#### 7. Authentication Status
- **URL**: `GET /api/auth/status/`
- **Description**: Check if user is authenticated
- **Authentication**: Required (Bearer token)

## JWT Configuration

### Token Settings
- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 1 day
- **Token Rotation**: Enabled (new refresh token on each refresh)
- **Blacklisting**: Enabled (tokens are blacklisted after rotation)
- **Algorithm**: HS256

### Authentication Header
Use Bearer token in the Authorization header:
```
Authorization: Bearer your_jwt_access_token_here
```

## Usage Examples

### 1. Register a New User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "first_name": "New",
    "last_name": "User",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### 2. Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepassword123"
  }'
```

### 3. Access Protected Endpoint
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer your_access_token_here"
```

## Security Features

1. **Password Validation**: Minimum 8 characters required
2. **Token Expiration**: Automatic token expiration for security
3. **Token Blacklisting**: Logout properly blacklists refresh tokens
4. **CORS Configuration**: Properly configured for frontend integration
5. **Permission Classes**: Protected endpoints require authentication

## Integration with Other Apps

The authentication system is integrated with Django REST Framework and can be used to protect any endpoint in other apps by adding:

```python
from rest_framework.permissions import IsAuthenticated

class YourProtectedView(APIView):
    permission_classes = [IsAuthenticated]
```

## Testing

A comprehensive test script is provided (`test_jwt_auth.py`) that tests:
- User registration
- User login
- Protected endpoint access
- Token refresh functionality
- Authentication status

Run the test with:
```bash
python test_jwt_auth.py
```

## Swagger Documentation

Access the interactive API documentation at:
- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/

## Files Structure

```
auth_app/
├── __init__.py
├── admin.py          # Admin configuration
├── apps.py           # App configuration
├── models.py         # Uses Django's built-in User model
├── serializers.py    # DRF serializers for authentication
├── tests.py          # Unit tests (to be implemented)
├── urls.py           # URL routing
└── views.py          # API views and logic
```

## Dependencies

- Django 5.1.2
- djangorestframework 3.15.2
- djangorestframework-simplejwt 5.5.1
- PyJWT 2.10.1

The authentication app is now fully functional and ready for production use!