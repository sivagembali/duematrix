"""
Seed script to create roles and dummy users
Run this script after database migrations
"""

from app import create_app
from models import db, RoleMaster, RoleMapping, User
from datetime import datetime

def seed_roles():
    """Create the three roles"""
    print("\n" + "="*50)
    print("Creating Roles...")
    print("="*50)
    
    roles_data = [
        {
            'role_name': 'Admin',
            'role_description': 'Administrator with full system access',
            'is_active': True
        },
        {
            'role_name': 'Telecaller',
            'role_description': 'Telecaller role for making calls and managing leads',
            'is_active': True
        },
        {
            'role_name': 'Field Agent',
            'role_description': 'Field agent for on-site visits and data collection',
            'is_active': True
        }
    ]
    
    created_roles = []
    for role_data in roles_data:
        # Check if role already exists
        existing_role = RoleMaster.query.filter_by(role_name=role_data['role_name']).first()
        if existing_role:
            print(f"✓ Role '{role_data['role_name']}' already exists (ID: {existing_role.id})")
            created_roles.append(existing_role)
        else:
            role = RoleMaster.from_dict(role_data)
            db.session.add(role)
            db.session.flush()  # Get the ID without committing
            print(f"✓ Created role: {role_data['role_name']} (ID: {role.id})")
            created_roles.append(role)
    
    db.session.commit()
    return created_roles


def seed_users(roles):
    """Create three dummy users"""
    print("\n" + "="*50)
    print("Creating Dummy Users...")
    print("="*50)
    
    users_data = [
        {
            'username': 'admin_user',
            'email': 'admin@duematrix.com',
            'password': 'Admin@123',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_active': True,
            'is_verified': True
        },
        {
            'username': 'telecaller_user',
            'email': 'telecaller@duematrix.com',
            'password': 'Tele@123',
            'first_name': 'Tele',
            'last_name': 'Caller',
            'is_active': True,
            'is_verified': True
        },
        {
            'username': 'fieldagent_user',
            'email': 'fieldagent@duematrix.com',
            'password': 'Field@123',
            'first_name': 'Field',
            'last_name': 'Agent',
            'is_active': True,
            'is_verified': True
        }
    ]
    
    created_users = []
    for user_data in users_data:
        # Check if user already exists
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if existing_user:
            print(f"✓ User '{user_data['username']}' already exists (ID: {existing_user.id})")
            created_users.append(existing_user)
        else:
            user = User.from_dict(user_data)
            db.session.add(user)
            db.session.flush()  # Get the ID without committing
            print(f"✓ Created user: {user_data['username']} (ID: {user.id})")
            print(f"  Email: {user_data['email']}")
            print(f"  Password: {user_data['password']}")
            created_users.append(user)
    
    db.session.commit()
    return created_users


def seed_role_mappings(users, roles):
    """Map each user to their respective role"""
    print("\n" + "="*50)
    print("Creating Role Mappings...")
    print("="*50)
    
    # Map: Admin user -> Admin role, Telecaller user -> Telecaller role, Field Agent user -> Field Agent role
    mappings = [
        {'user': users[0], 'role': roles[0]},  # admin_user -> Admin
        {'user': users[1], 'role': roles[1]},  # telecaller_user -> Telecaller
        {'user': users[2], 'role': roles[2]}   # fieldagent_user -> Field Agent
    ]
    
    for mapping_data in mappings:
        user = mapping_data['user']
        role = mapping_data['role']
        
        # Check if mapping already exists
        existing_mapping = RoleMapping.query.filter_by(
            user_id=user.id,
            role_id=role.id
        ).first()
        
        if existing_mapping:
            if existing_mapping.is_active:
                print(f"✓ Mapping already exists: {user.username} -> {role.role_name}")
            else:
                # Reactivate
                existing_mapping.is_active = True
                existing_mapping.revoked_at = None
                print(f"✓ Reactivated mapping: {user.username} -> {role.role_name}")
        else:
            role_mapping = RoleMapping(
                user_id=user.id,
                role_id=role.id,
                is_active=True,
                assigned_at=datetime.utcnow()
            )
            db.session.add(role_mapping)
            print(f"✓ Created mapping: {user.username} -> {role.role_name}")
    
    db.session.commit()


def main():
    """Main seeding function"""
    print("\n" + "="*50)
    print("ROLE & USER SEEDING SCRIPT")
    print("="*50)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create roles
            roles = seed_roles()
            
            # Create users
            users = seed_users(roles)
            
            # Create role mappings
            seed_role_mappings(users, roles)
            
            print("\n" + "="*50)
            print("✅ SEEDING COMPLETED SUCCESSFULLY!")
            print("="*50)
            
            print("\n📋 Summary:")
            print(f"   Roles created: {len(roles)}")
            print(f"   Users created: {len(users)}")
            print(f"   Role mappings created: {len(users)}")
            
            print("\n👥 User Credentials:")
            print("   1. Admin User:")
            print("      Username: admin_user")
            print("      Email: admin@duematrix.com")
            print("      Password: Admin@123")
            print("      Role: Admin")
            
            print("\n   2. Telecaller User:")
            print("      Username: telecaller_user")
            print("      Email: telecaller@duematrix.com")
            print("      Password: Tele@123")
            print("      Role: Telecaller")
            
            print("\n   3. Field Agent User:")
            print("      Username: fieldagent_user")
            print("      Email: fieldagent@duematrix.com")
            print("      Password: Field@123")
            print("      Role: Field Agent")
            
            print("\n🚀 You can now login with these credentials!")
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"\n❌ Error during seeding: {str(e)}")
            db.session.rollback()
            raise


if __name__ == "__main__":
    main()
