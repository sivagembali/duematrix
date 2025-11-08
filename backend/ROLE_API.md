# Role Management API Documentation

## Overview
The DueMatrix backend provides comprehensive role management with role master definitions, user-role mappings, and relationship tracking.

## Database Schema

### Tables

#### 1. role_master
Stores role definitions and metadata.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| role_name | VARCHAR(100) | Unique role name (indexed) |
| role_description | VARCHAR(255) | Role description |
| is_active | BOOLEAN | Role active status |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | INTEGER | Creator user ID |
| updated_by | INTEGER | Last updater user ID |

#### 2. role_mapping
Stores user-to-role assignments.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| user_id | INTEGER | Foreign key to users table |
| role_id | INTEGER | Foreign key to role_master table |
| is_active | BOOLEAN | Mapping active status |
| assigned_at | TIMESTAMP | Assignment timestamp |
| revoked_at | TIMESTAMP | Revocation timestamp |
| assigned_by | INTEGER | Assigner user ID |
| revoked_by | INTEGER | Revoker user ID |

**Constraints:**
- `unique_user_role`: Unique constraint on (user_id, role_id)
- Foreign keys with CASCADE delete

---

## API Endpoints

### Base URL
```
http://localhost:5000/api
```

All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

---

### 1. Get All Roles
Retrieve all role definitions.

**Endpoint:** `GET /api/roles`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "role_name": "Admin",
      "role_description": "Administrator with full system access",
      "is_active": true,
      "created_at": "2025-11-08T12:40:06",
      "updated_at": "2025-11-08T12:40:06",
      "created_by": null,
      "updated_by": null
    }
  ]
}
```

---

### 2. Get Single Role
Retrieve a specific role by ID.

**Endpoint:** `GET /api/roles/<role_id>`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "role_name": "Admin",
    "role_description": "Administrator with full system access",
    "is_active": true,
    "created_at": "2025-11-08T12:40:06",
    "updated_at": "2025-11-08T12:40:06",
    "created_by": null,
    "updated_by": null
  }
}
```

---

### 3. Create Role
Create a new role (Admin only recommended).

**Endpoint:** `POST /api/roles`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "role_name": "Manager",
  "role_description": "Manager role with team oversight",
  "is_active": true
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Role created successfully",
  "data": {
    "id": 4,
    "role_name": "Manager",
    "role_description": "Manager role with team oversight",
    "is_active": true,
    "created_at": "2025-11-08T12:45:00",
    "updated_at": "2025-11-08T12:45:00",
    "created_by": 1,
    "updated_by": null
  }
}
```

**Error (409 Conflict):**
```json
{
  "success": false,
  "error": "Role already exists"
}
```

---

### 4. Update Role
Update an existing role.

**Endpoint:** `PUT /api/roles/<role_id>`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "role_description": "Updated description",
  "is_active": false
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Role updated successfully",
  "data": {
    "id": 1,
    "role_name": "Admin",
    "role_description": "Updated description",
    "is_active": false,
    "created_at": "2025-11-08T12:40:06",
    "updated_at": "2025-11-08T12:50:00",
    "created_by": null,
    "updated_by": 1
  }
}
```

---

### 5. Assign Role to User
Create a user-role mapping.

**Endpoint:** `POST /api/role-mappings`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "user_id": 1,
  "role_id": 2
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Role assigned to user successfully",
  "data": {
    "id": 4,
    "user_id": 1,
    "role_id": 2,
    "is_active": true,
    "assigned_at": "2025-11-08T12:55:00",
    "revoked_at": null,
    "assigned_by": 1,
    "revoked_by": null
  }
}
```

**Error (409 Conflict):**
```json
{
  "success": false,
  "error": "User already has this role"
}
```

---

### 6. Revoke Role from User
Revoke a user-role mapping (soft delete).

**Endpoint:** `DELETE /api/role-mappings/<mapping_id>`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Role revoked from user successfully"
}
```

---

### 7. Get User's Roles
Retrieve all active roles for a specific user.

**Endpoint:** `GET /api/users/<user_id>/roles`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "username": "admin_user",
    "roles": [
      {
        "id": 1,
        "role_name": "Admin",
        "role_description": "Administrator with full system access",
        "is_active": true,
        "mapping_id": 1,
        "assigned_at": "2025-11-08T12:40:06",
        "created_at": "2025-11-08T12:40:06",
        "updated_at": "2025-11-08T12:40:06",
        "created_by": null,
        "updated_by": null
      }
    ]
  }
}
```

---

### 8. Get Role's Users
Retrieve all users with a specific role.

**Endpoint:** `GET /api/roles/<role_id>/users`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "role_id": 1,
    "role_name": "Admin",
    "users": [
      {
        "id": 1,
        "username": "admin_user",
        "email": "admin@duematrix.com",
        "first_name": "Admin",
        "last_name": "User",
        "is_active": true,
        "is_verified": true,
        "mapping_id": 1,
        "assigned_at": "2025-11-08T12:40:06",
        "created_at": "2025-11-08T12:40:06",
        "updated_at": "2025-11-08T12:40:06",
        "last_login": null
      }
    ]
  }
}
```

---

## Seeded Roles & Users

### Default Roles

1. **Admin**
   - Full system access
   - Can manage users, roles, and all data

2. **Telecaller**
   - Make calls and manage leads
   - Limited data access

3. **Field Agent**
   - On-site visits and data collection
   - Mobile-optimized features

### Default Users

| Username | Email | Password | Role |
|----------|-------|----------|------|
| admin_user | admin@duematrix.com | Admin@123 | Admin |
| telecaller_user | telecaller@duematrix.com | Tele@123 | Telecaller |
| fieldagent_user | fieldagent@duematrix.com | Field@123 | Field Agent |

---

## Usage Examples

### cURL Examples

```bash
# 1. Login as admin
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin_user","password":"Admin@123"}'

# Save the access_token from response

# 2. Get all roles
curl -X GET http://localhost:5000/api/roles \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 3. Get user's roles
curl -X GET http://localhost:5000/api/users/1/roles \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 4. Assign role to user
curl -X POST http://localhost:5000/api/role-mappings \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":2,"role_id":1}'

# 5. Get users with specific role
curl -X GET http://localhost:5000/api/roles/2/users \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Angular Service Example

```typescript
// role.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class RoleService {
  private apiUrl = 'http://localhost:5000/api';
  
  constructor(private http: HttpClient) {}
  
  private getHeaders(token: string): HttpHeaders {
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }
  
  getAllRoles(token: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/roles`, { 
      headers: this.getHeaders(token) 
    });
  }
  
  getUserRoles(userId: number, token: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/${userId}/roles`, {
      headers: this.getHeaders(token)
    });
  }
  
  assignRole(userId: number, roleId: number, token: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/role-mappings`, 
      { user_id: userId, role_id: roleId },
      { headers: this.getHeaders(token) }
    );
  }
  
  revokeRole(mappingId: number, token: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/role-mappings/${mappingId}`, {
      headers: this.getHeaders(token)
    });
  }
}
```

---

## Database Relationships

```
users (1) ----< (N) role_mapping (N) >---- (1) role_master
```

- One user can have multiple roles (many-to-many through role_mapping)
- Soft delete: revoke by setting `is_active = false` and `revoked_at` timestamp
- Cascade delete: deleting user or role removes all mappings

---

## Running the Seed Script

```bash
# Seed roles and users
python seed_roles_users.py
```

This script:
- Creates 3 roles (Admin, Telecaller, Field Agent)
- Creates 3 users (one for each role)
- Maps each user to their respective role
- Is idempotent (safe to run multiple times)

---

## Security Considerations

1. **Authorization:** Implement role-based access control in endpoints
2. **Admin Actions:** Restrict role creation/updates to admin users
3. **Audit Trail:** Track who assigns/revokes roles via assigned_by/revoked_by
4. **Soft Delete:** Never hard-delete role mappings (maintain history)
5. **Validation:** Verify role/user existence before assignment

---

## Next Steps

1. **Implement RBAC middleware** for endpoint protection
2. **Add permissions system** for granular access control
3. **Create role hierarchy** (e.g., Admin > Manager > User)
4. **Add role-based column filtering** using column_headers.role_id
5. **Build admin dashboard** for role management UI

---

## Status: ✅ COMPLETE

Role management system is fully implemented with:
- 2 database tables (role_master, role_mapping)
- 8 REST API endpoints
- 3 seeded roles
- 3 seeded users with role mappings
- Comprehensive relationships and constraints
