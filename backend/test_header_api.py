#!/usr/bin/env python3
"""
API Test Script for Header Configuration Endpoints
Tests all the header configuration API endpoints to ensure they work correctly.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000/api"
HEADERS = {"Content-Type": "application/json"}

def test_endpoint(method, endpoint, data=None, params=None):
    """Test a specific API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, params=params, headers=HEADERS)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=HEADERS)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=HEADERS)
        elif method.upper() == 'PATCH':
            response = requests.patch(url, json=data, headers=HEADERS)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=HEADERS)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        print(f"{method.upper()} {endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ Success")
            result = response.json()
            if 'data' in result:
                if isinstance(result['data'], list):
                    print(f"   Returned {len(result['data'])} items")
                else:
                    print(f"   Data type: {type(result['data'])}")
            print()
            return True
        else:
            print(f"❌ Failed: {response.text}")
            print()
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed to {url}")
        print("   Make sure the Flask server is running on port 5000")
        print()
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        return False

def main():
    """Run all API tests"""
    print("🧪 Testing Header Configuration API Endpoints")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Get all header configurations
    total_tests += 1
    if test_endpoint('GET', '/header-config'):
        tests_passed += 1
    
    # Test 2: Get visible columns only
    total_tests += 1
    if test_endpoint('GET', '/header-config', params={'visible_only': 'true'}):
        tests_passed += 1
    
    # Test 3: Get bills with configuration (main endpoint for frontend)
    total_tests += 1
    if test_endpoint('GET', '/header-config/bills-with-config', 
                    params={'page': 1, 'per_page': 10}):
        tests_passed += 1
    
    # Test 4: Get bills with search
    total_tests += 1
    if test_endpoint('GET', '/header-config/bills-with-config', 
                    params={'search': 'test', 'status': 'pending'}):
        tests_passed += 1
    
    # Test 5: Toggle column visibility
    total_tests += 1
    if test_endpoint('PATCH', '/header-config/toggle-visibility/sNo', 
                    data={'visible': False}):
        tests_passed += 1
    
    # Test 6: Reset to defaults
    total_tests += 1
    if test_endpoint('POST', '/header-config/reset-defaults'):
        tests_passed += 1
    
    # Test 7: Bulk update configurations
    total_tests += 1
    bulk_data = {
        'configs': [
            {'id': 1, 'status': True, 'width': 150},
            {'id': 2, 'status': False, 'width': 200}
        ]
    }
    if test_endpoint('PUT', '/header-config/bulk-update', data=bulk_data):
        tests_passed += 1
    
    # Test 8: Update display order
    total_tests += 1
    order_data = {
        'columnOrders': [
            {'colName': 'sNo', 'displayOrder': 1},
            {'colName': 'cardNo', 'displayOrder': 2}
        ]
    }
    if test_endpoint('PATCH', '/header-config/display-order', data=order_data):
        tests_passed += 1
    
    # Test 9: Get specific column configuration
    total_tests += 1
    if test_endpoint('GET', '/header-config/column/sNo'):
        tests_passed += 1
    
    # Summary
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The Header Configuration API is working correctly.")
    else:
        print(f"⚠️  {total_tests - tests_passed} test(s) failed. Check the server logs for details.")
    
    print("\n📝 Available Endpoints:")
    print("   GET    /api/header-config")
    print("   GET    /api/header-config/bills-with-config")
    print("   GET    /api/header-config/column/{colName}")
    print("   PATCH  /api/header-config/toggle-visibility/{colName}")
    print("   PUT    /api/header-config/bulk-update")
    print("   POST   /api/header-config/reset-defaults")
    print("   PATCH  /api/header-config/display-order")

if __name__ == "__main__":
    main()