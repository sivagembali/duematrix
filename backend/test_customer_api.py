import requests
import json

# Base URL
BASE_URL = 'http://localhost:5000'

def test_login():
    """Test login and get JWT token"""
    print("\n=== Testing Login ===")
    response = requests.post(f'{BASE_URL}/api/auth/login', json={
        'username': 'admin_user',
        'password': 'Admin@123'
    })
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        token = response.json().get('data', {}).get('access_token')
        print(f"\n✅ Login successful! Token: {token[:20]}...")
        return token
    else:
        print("\n❌ Login failed!")
        return None

def test_get_customer_data(token):
    """Test fetching customer data"""
    print("\n=== Testing Get Customer Data ===")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Test without filters
    response = requests.get(f'{BASE_URL}/api/data/customer-data', headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
        print(f"Total Records: {data.get('pagination', {}).get('total')}")
        print(f"Records Returned: {len(data.get('data', []))}")
        
        # Print first record
        if data.get('data'):
            first_record = data['data'][0]
            print(f"\nFirst Record:")
            print(f"  ID: {first_record.get('id')}")
            print(f"  Name: {first_record.get('customer_name')}")
            print(f"  Email: {first_record.get('email')}")
            print(f"  Bank: {first_record.get('bank')}")
            print(f"  Cycle: {first_record.get('cycle_name')}")
            print(f"  User ID: {first_record.get('user_id')}")
        
        print("\n✅ Customer data fetch successful!")
        return True
    else:
        print(f"Response: {response.text}")
        print("\n❌ Customer data fetch failed!")
        return False

def test_get_customer_data_with_filters(token):
    """Test fetching customer data with filters"""
    print("\n=== Testing Get Customer Data with Filters ===")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Test with filters
    params = {
        'department': 'Engineering',
        'per_page': 10
    }
    
    response = requests.get(f'{BASE_URL}/api/data/customer-data', headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Total Records: {data.get('pagination', {}).get('total')}")
        print(f"Records Returned: {len(data.get('data', []))}")
        print("\n✅ Filtered customer data fetch successful!")
        return True
    else:
        print(f"Response: {response.text}")
        print("\n❌ Filtered customer data fetch failed!")
        return False

def test_get_filter_options(token):
    """Test fetching filter options"""
    print("\n=== Testing Get Filter Options ===")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(f'{BASE_URL}/api/data/customer-data/filters', headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        
        filters = data.get('data', {})
        print(f"\nAvailable Filters:")
        print(f"  Departments: {len(filters.get('departments', []))} - {filters.get('departments', [])[:3]}")
        print(f"  Statuses: {len(filters.get('statuses', []))} - {filters.get('statuses', [])}")
        print(f"  Cities: {len(filters.get('cities', []))} - {filters.get('cities', [])[:3]}")
        print(f"  Banks: {len(filters.get('banks', []))} - {filters.get('banks', [])}")
        print(f"  Cycles: {len(filters.get('cycles', []))} - {filters.get('cycles', [])}")
        
        print("\n✅ Filter options fetch successful!")
        return True
    else:
        print(f"Response: {response.text}")
        print("\n❌ Filter options fetch failed!")
        return False

def main():
    print("=" * 60)
    print("Customer Data API Integration Test")
    print("=" * 60)
    
    # Step 1: Login
    token = test_login()
    if not token:
        print("\n❌ Cannot proceed without token. Please ensure Flask app is running.")
        return
    
    # Step 2: Get customer data
    test_get_customer_data(token)
    
    # Step 3: Get customer data with filters
    test_get_customer_data_with_filters(token)
    
    # Step 4: Get filter options
    test_get_filter_options(token)
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
