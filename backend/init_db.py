#!/usr/bin/env python3
"""
Initialize database with migrations and seed data
Run this as a one-time job on Render
"""
import os
import sys

# Add backend to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from flask_migrate import upgrade

print("Starting database initialization...")

with app.app_context():
    print("Running migrations...")
    try:
        upgrade()
        print("✓ Migrations completed")
    except Exception as e:
        print(f"Migration error (might be okay if tables exist): {e}")
    
    # Create tables if they don't exist
    print("Creating tables...")
    db.create_all()
    print("✓ Tables created")

# Import and run seed scripts
print("\nSeeding data...")

try:
    print("1. Seeding roles and users...")
    import seed_roles_users
    # Run the seeding script's main() to actually seed data
    try:
        seed_roles_users.main()
        print("✓ Roles and users seeded")
    except Exception as e:
        print(f"Error running seed_roles_users.main(): {e}")
except Exception as e:
    print(f"Error seeding roles/users: {e}")

try:
    print("2. Seeding headers...")
    import seed_comprehensive_headers
        # Try to run the module's main(), otherwise call known seed function
        try:
            if hasattr(seed_comprehensive_headers, 'main'):
                seed_comprehensive_headers.main()
            elif hasattr(seed_comprehensive_headers, 'seed_comprehensive_headers'):
                seed_comprehensive_headers.seed_comprehensive_headers()
            else:
                raise AttributeError('No entry function found in seed_comprehensive_headers')
            print("✓ Headers seeded")
        except Exception as e:
            print(f"Error running seed_comprehensive_headers: {e}")
except Exception as e:
    print(f"Error seeding headers: {e}")

try:
    print("3. Seeding cycles...")
    import seed_cycles
        try:
            if hasattr(seed_cycles, 'main'):
                seed_cycles.main()
            elif hasattr(seed_cycles, 'seed_cycles'):
                # Ensure app context is present
                seed_cycles.seed_cycles()
            else:
                raise AttributeError('No entry function found in seed_cycles')
            print("✓ Cycles seeded")
        except Exception as e:
            print(f"Error running seed_cycles: {e}")
except Exception as e:
    print(f"Error seeding cycles: {e}")

try:
    print("4. Seeding customer data...")
    import seed_customer_data
        try:
            if hasattr(seed_customer_data, 'main'):
                seed_customer_data.main()
            elif hasattr(seed_customer_data, 'seed_customer_data'):
                # default to 100 records
                seed_customer_data.seed_customer_data(100)
            else:
                raise AttributeError('No entry function found in seed_customer_data')
            print("✓ Customer data seeded")
        except Exception as e:
            print(f"Error running seed_customer_data: {e}")
except Exception as e:
    print(f"Error seeding customer data: {e}")

print("\n✅ Database initialization complete!")
