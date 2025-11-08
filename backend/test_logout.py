"""
Test logout API with proper JWT token
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/auth"

# Step 1: Login to get a valid token
print("\n" + "="*60)
print("STEP 1: LOGIN")
print("="*60)

login_data = {
    "username": "admin_user",
    "password": "Admin@123"
}

login_response = requests.post(f"{BASE_URL}/login", json=login_data)
print(f"Login Status: {login_response.status_code}")
print(f"Login Response: {json.dumps(login_response.json(), indent=2)}")

if login_response.status_code == 200:
    access_token = login_response.json()['data']['access_token']
    print(f"\nAccess Token (first 50 chars): {access_token[:50]}...")
    
    # Step 2: Test logout with the token
    print("\n" + "="*60)
    print("STEP 2: LOGOUT")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    print(f"Authorization Header: Bearer {access_token[:30]}...")
    
    logout_response = requests.post(f"{BASE_URL}/logout", headers=headers)
    print(f"\nLogout Status: {logout_response.status_code}")
    print(f"Logout Response: {json.dumps(logout_response.json(), indent=2)}")
    
    if logout_response.status_code == 200:
        print("\n✓ LOGOUT SUCCESSFUL!")
    else:
        print("\n✗ LOGOUT FAILED!")
        print(f"Error: {logout_response.json()}")
else:
    print("\n✗ LOGIN FAILED - Cannot test logout")
