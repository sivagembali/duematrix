"""
Debug script to check users in database and test password hashing
"""

from app import create_app
from models import db, User
from flask_bcrypt import check_password_hash

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("CHECKING USERS IN DATABASE")
    print("="*60)
    
    users = User.query.all()
    
    if not users:
        print("\n❌ No users found in database!")
        print("Run: python seed_roles_users.py")
    else:
        print(f"\n✓ Found {len(users)} users\n")
        
        for user in users:
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"First Name: {user.first_name}")
            print(f"Last Name: {user.last_name}")
            print(f"Is Active: {user.is_active}")
            print(f"Is Verified: {user.is_verified}")
            print(f"Password Hash: {user.password_hash[:50]}...")
            
            # Test password
            test_passwords = ['Admin@123', 'Tele@123', 'Field@123']
            print("\nTesting passwords:")
            for pwd in test_passwords:
                result = user.check_password(pwd)
                symbol = "✓" if result else "✗"
                print(f"  {symbol} Password '{pwd}': {result}")
            
            print("\n" + "-"*60 + "\n")
    
    # Test specific login
    print("\n" + "="*60)
    print("TESTING LOGIN FOR admin_user")
    print("="*60)
    
    admin_user = User.query.filter_by(username='admin_user').first()
    if admin_user:
        print(f"\n✓ Found user: {admin_user.username}")
        print(f"  Email: {admin_user.email}")
        print(f"  Active: {admin_user.is_active}")
        
        # Test the exact password
        test_password = 'Admin@123'
        result = admin_user.check_password(test_password)
        
        print(f"\n  Testing password '{test_password}': {result}")
        
        if result:
            print("  ✓ Password is CORRECT - Login should work!")
        else:
            print("  ✗ Password is WRONG - There's an issue with password hashing")
            print(f"  Stored hash: {admin_user.password_hash}")
    else:
        print("\n❌ admin_user not found in database!")
        print("Run: python seed_roles_users.py")
