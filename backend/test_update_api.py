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
    
    if response.status_code == 200:
        token = response.json().get('data', {}).get('access_token')
        print(f"✅ Login successful!")
        return token
    else:
        print(f"❌ Login failed: {response.json()}")
        return None

def test_update_customer(token):
    """Test updating a customer record"""
    print("\n=== Testing Update Customer Data ===")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # First, get a record to update
    response = requests.get(f'{BASE_URL}/api/data/customer-data?per_page=1', headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to get customer data: {response.status_code}")
        return False
    
    data = response.json()
    if not data.get('data') or len(data['data']) == 0:
        print("❌ No customer data found")
        return False
    
    customer = data['data'][0]
    customer_id = customer['id']
    original_email = customer['email']
    
    print(f"Original customer:")
    print(f"  ID: {customer_id}")
    print(f"  Name: {customer['customer_name']}")
    print(f"  Email: {original_email}")
    print(f"  City: {customer.get('city', 'N/A')}")
    print(f"  Bank: {customer.get('bank', 'N/A')}")
    
    # Update the customer
    update_data = {
        'city': 'Updated City - Mumbai',
        'notes': 'Updated via API test - ' + str(customer_id)
    }
    
    print(f"\nUpdating customer {customer_id} with:")
    print(json.dumps(update_data, indent=2))
    
    response = requests.put(
        f'{BASE_URL}/api/data/customer-data/{customer_id}',
        headers=headers,
        json=update_data
    )
    
    print(f"\nUpdate Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        updated_customer = response.json().get('data', {})
        print(f"\n✅ Update successful!")
        print(f"Updated customer:")
        print(f"  ID: {updated_customer.get('id')}")
        print(f"  Name: {updated_customer.get('customer_name')}")
        print(f"  Email: {updated_customer.get('email')}")
        print(f"  City: {updated_customer.get('city')}")
        print(f"  Notes: {updated_customer.get('notes')}")
        return True
    else:
        print(f"❌ Update failed!")
        return False

def main():
    print("=" * 60)
    print("Customer Data Update API Test")
    print("=" * 60)
    
    # Step 1: Login
    token = test_login()
    if not token:
        print("\n❌ Cannot proceed without token. Please ensure Flask app is running.")
        return
    
    # Step 2: Test update
    test_update_customer(token)
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
