"""
Test script for authentication endpoints
Run this after starting the Flask server
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/auth"

def test_register():
    """Test user registration"""
    print("\n" + "="*50)
    print("Testing User Registration")
    print("="*50)
    
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json()['data']['access_token']
    return None


def test_login():
    """Test user login"""
    print("\n" + "="*50)
    print("Testing User Login")
    print("="*50)
    
    data = {
        "username": "testuser",
        "password": "TestPass123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()['data']['access_token'], response.json()['data']['refresh_token']
    return None, None


def test_get_current_user(access_token):
    """Test getting current user"""
    print("\n" + "="*50)
    print("Testing Get Current User")
    print("="*50)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_change_password(access_token):
    """Test changing password"""
    print("\n" + "="*50)
    print("Testing Change Password")
    print("="*50)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    data = {
        "current_password": "TestPass123",
        "new_password": "NewTestPass456"
    }
    
    response = requests.put(f"{BASE_URL}/change-password", json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_refresh_token(refresh_token):
    """Test refreshing access token"""
    print("\n" + "="*50)
    print("Testing Refresh Token")
    print("="*50)
    
    headers = {
        "Authorization": f"Bearer {refresh_token}"
    }
    
    response = requests.post(f"{BASE_URL}/refresh", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()['data']['access_token']
    return None


def test_logout(access_token):
    """Test logout"""
    print("\n" + "="*50)
    print("Testing Logout")
    print("="*50)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.post(f"{BASE_URL}/logout", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("AUTHENTICATION API TESTS")
    print("="*50)
    print("Make sure Flask server is running on http://localhost:5000")
    input("Press Enter to continue...")
    
    try:
        # Test registration (comment out if user already exists)
        # access_token = test_register()
        
        # Test login
        access_token, refresh_token = test_login()
        
        if not access_token:
            print("\n❌ Login failed! Cannot continue tests.")
            return
        
        # Test get current user
        test_get_current_user(access_token)
        
        # Test refresh token
        new_access_token = test_refresh_token(refresh_token)
        if new_access_token:
            access_token = new_access_token
        
        # Test change password (optional - will change password!)
        # test_change_password(access_token)
        
        # Test logout
        test_logout(access_token)
        
        print("\n" + "="*50)
        print("✅ All tests completed!")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to Flask server")
        print("Make sure the server is running: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
