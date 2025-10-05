#!/usr/bin/env python3
"""
Test script for JWT Authentication API
Run this script to test the authentication endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/auth"

def test_user_registration():
    """Test user registration endpoint"""
    print("Testing User Registration...")
    
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword123",
        "password_confirm": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201

def test_user_login():
    """Test user login endpoint"""
    print("\nTesting User Login...")
    
    data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        tokens = response.json()
        print("Login successful!")
        print(f"Access Token: {tokens['access'][:50]}...")
        print(f"Refresh Token: {tokens['refresh'][:50]}...")
        print(f"User Info: {tokens['user']}")
        return tokens
    else:
        print(f"Login failed: {response.json()}")
        return None

def test_protected_endpoint(access_token):
    """Test a protected endpoint"""
    print("\nTesting Protected Endpoint (User Profile)...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_auth_status(access_token):
    """Test authentication status endpoint"""
    print("\nTesting Authentication Status...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/status/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_token_refresh(refresh_token):
    """Test token refresh endpoint"""
    print("\nTesting Token Refresh...")
    
    data = {
        "refresh": refresh_token
    }
    
    response = requests.post(f"{BASE_URL}/token/refresh/", json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        new_tokens = response.json()
        print("Token refresh successful!")
        print(f"New Access Token: {new_tokens['access'][:50]}...")
        return new_tokens['access']
    else:
        print(f"Token refresh failed: {response.json()}")
        return None

def main():
    """Main test function"""
    print("=== JWT Authentication API Test ===")
    
    # Test registration
    if not test_user_registration():
        print("Registration failed, trying to login with existing user...")
    
    # Test login
    tokens = test_user_login()
    if not tokens:
        print("Login failed! Exiting...")
        return
    
    access_token = tokens['access']
    refresh_token = tokens['refresh']
    
    # Test protected endpoints
    test_protected_endpoint(access_token)
    test_auth_status(access_token)
    
    # Test token refresh
    new_access_token = test_token_refresh(refresh_token)
    if new_access_token:
        print("\nTesting with new access token...")
        test_auth_status(new_access_token)
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure Django is running on http://127.0.0.1:8000/")
    except Exception as e:
        print(f"Error: {e}")