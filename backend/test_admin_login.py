"""
Quick test script to verify admin_user login works
"""

import requests
import json

print("\n" + "="*60)
print("TESTING LOGIN WITH admin_user")
print("="*60)

url = "http://localhost:5000/api/auth/login"
data = {
    "username": "admin_user",
    "password": "Admin@123"
}

print(f"\nSending POST request to: {url}")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n✓ LOGIN SUCCESSFUL!")
        print(f"User: {response.json()['data']['user']['username']}")
        print(f"Email: {response.json()['data']['user']['email']}")
    else:
        print("\n✗ LOGIN FAILED!")
        
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
