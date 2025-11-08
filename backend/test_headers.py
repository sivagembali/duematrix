"""
Test script to verify the headers API endpoints
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000/api"
LOGIN_URL = f"{BASE_URL}/auth/login"
HEADERS_URL = f"{BASE_URL}/headers/dashboard"

def test_headers_api():
    """Test the headers API with authentication"""
    
    # Step 1: Login to get JWT token
    print("Step 1: Logging in...")
    login_data = {
        "username": "admin_user",
        "password": "Admin@123"
    }
    
    login_response = requests.post(LOGIN_URL, json=login_data)
    
    if login_response.status_code != 200:
        print("❌ Login failed!")
        print(login_response.json())
        return
    
    login_result = login_response.json()
    print("Login response:", json.dumps(login_result, indent=2))
    
    # Handle nested data structure
    data = login_result.get('data', login_result)
    access_token = data.get('access_token') or data.get('token')
    user_data = data.get('user', {})
    
    if not access_token:
        print("❌ No access token in response!")
        return
        
    print("✓ Login successful!")
    print(f"User: {user_data.get('username', 'N/A')}")
    print(f"Role: {user_data.get('role_name', 'N/A')}")
    
    # Step 2: Get dashboard headers
    print("\nStep 2: Fetching dashboard headers...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    headers_response = requests.get(HEADERS_URL, headers=headers)
    
    if headers_response.status_code != 200:
        print("❌ Failed to fetch headers!")
        print(headers_response.json())
        return
    
    headers_result = headers_response.json()
    print("✓ Headers fetched successfully!")
    print(f"\nTotal headers: {headers_result['count']}")
    
    # Display header details
    print("\n" + "="*80)
    print("COLUMN HEADERS CONFIGURATION")
    print("="*80)
    
    for header in headers_result['data']:
        print(f"\n{header['display_order']}. {header['col_label']} ({header['col_header']})")
        print(f"   Width: {header['col_width']} rem")
        print(f"   Editable: {header['is_editable']}")
        print(f"   Multi-Select: {header['is_multi_select']}")
        print(f"   Display: {header['display']}")
        print(f"   Default Display: {header['default_display']}")
        print(f"   Frozen: {header['is_frozen']}")
        print(f"   Role: {'Specific Role' if header['role_id'] else 'All Roles'}")
    
    print("\n" + "="*80)
    
    # Display user info
    if 'user' in headers_result:
        user_info = headers_result['user']
        print(f"\nUser Info:")
        print(f"  ID: {user_info['id']}")
        print(f"  Username: {user_info['username']}")
        print(f"  Role ID: {user_info['role_id']}")
    
    # Count different types
    default_headers = [h for h in headers_result['data'] if h['default_display']]
    role_specific = [h for h in headers_result['data'] if h['role_id']]
    
    print(f"\nSummary:")
    print(f"  - Total headers: {headers_result['count']}")
    print(f"  - Default display: {len(default_headers)}")
    print(f"  - Role-specific: {len(role_specific)}")
    print(f"  - Generic: {headers_result['count'] - len(role_specific)}")

if __name__ == '__main__':
    test_headers_api()
