# Authentication API Documentation

## Overview
The DueMatrix backend provides JWT-based authentication with secure password hashing using bcrypt. All authenticated endpoints require a valid JWT token in the Authorization header.

## Base URL
```
http://localhost:5000/api/auth
```

## Authentication Endpoints

### 1. Register User
Create a new user account.

**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "role_id": 1
}
```

**Required Fields:**
- `username` (string): Unique username
- `email` (string): Valid email address
- `password` (string): Must be at least 8 characters with uppercase, lowercase, and digit

**Optional Fields:**
- `first_name` (string)
- `last_name` (string)
- `role_id` (integer)

**Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role_id": 1,
      "is_active": true,
      "is_verified": false,
      "created_at": "2025-11-08T12:00:00",
      "updated_at": "2025-11-08T12:00:00",
      "last_login": null
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Error Responses:**
- `400`: Invalid input (missing fields, invalid email, weak password)
- `409`: Username or email already exists

---

### 2. Login
Authenticate user and receive JWT tokens.

**Endpoint:** `POST /api/auth/login`

**Request Body (Username):**
```json
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Request Body (Email):**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role_id": 1,
      "is_active": true,
      "is_verified": false,
      "created_at": "2025-11-08T12:00:00",
      "updated_at": "2025-11-08T12:00:00",
      "last_login": "2025-11-08T12:30:00"
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Error Responses:**
- `400`: Missing credentials
- `401`: Invalid credentials
- `403`: Account deactivated

---

### 3. Refresh Token
Get a new access token using a refresh token.

**Endpoint:** `POST /api/auth/refresh`

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Error Responses:**
- `401`: Invalid or expired refresh token

---

### 4. Get Current User
Get authenticated user's information.

**Endpoint:** `GET /api/auth/me`

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
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role_id": 1,
    "is_active": true,
    "is_verified": false,
    "created_at": "2025-11-08T12:00:00",
    "updated_at": "2025-11-08T12:00:00",
    "last_login": "2025-11-08T12:30:00"
  }
}
```

**Error Responses:**
- `401`: Missing or invalid token
- `404`: User not found

---

### 5. Change Password
Change authenticated user's password.

**Endpoint:** `PUT /api/auth/change-password`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "current_password": "SecurePass123",
  "new_password": "NewSecurePass456"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

**Error Responses:**
- `400`: Missing fields or weak new password
- `401`: Current password incorrect or invalid token

---

### 6. Logout
Logout user (client should delete tokens).

**Endpoint:** `POST /api/auth/logout`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

## Password Requirements
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)

## Email Validation
- Must be a valid email format
- Example: `user@example.com`

## JWT Token Configuration
- **Access Token Expiry:** 3600 seconds (1 hour)
- **Refresh Token Expiry:** 2592000 seconds (30 days)
- **Token Location:** Authorization header
- **Token Type:** Bearer

## Using Tokens in Requests

### With cURL
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"SecurePass123"}'

# Access protected endpoint
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### With JavaScript (Fetch)
```javascript
// Login
const response = await fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'johndoe',
    password: 'SecurePass123'
  })
});
const data = await response.json();
const accessToken = data.data.access_token;

// Access protected endpoint
const userResponse = await fetch('http://localhost:5000/api/auth/me', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

### With Angular HttpClient
```typescript
// auth.service.ts
import { HttpClient, HttpHeaders } from '@angular/common/http';

login(username: string, password: string) {
  return this.http.post('http://localhost:5000/api/auth/login', {
    username,
    password
  });
}

getCurrentUser(token: string) {
  const headers = new HttpHeaders({
    'Authorization': `Bearer ${token}`
  });
  return this.http.get('http://localhost:5000/api/auth/me', { headers });
}
```

## User Model Fields

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| username | String(80) | Unique username |
| email | String(120) | Unique email address |
| password_hash | String(255) | Hashed password (bcrypt) |
| first_name | String(100) | User's first name |
| last_name | String(100) | User's last name |
| role_id | Integer | Foreign key to roles table |
| is_active | Boolean | Account active status |
| is_verified | Boolean | Email verification status |
| created_at | DateTime | Account creation timestamp |
| updated_at | DateTime | Last update timestamp |
| last_login | DateTime | Last successful login |

## Security Features
- ✅ Password hashing with bcrypt
- ✅ JWT token-based authentication
- ✅ Password strength validation
- ✅ Email format validation
- ✅ Unique username and email constraints
- ✅ Account deactivation support
- ✅ Token expiration handling
- ✅ Secure token refresh mechanism

## Testing with Postman

1. **Create a new request collection**
2. **Register a user:**
   - Method: POST
   - URL: `http://localhost:5000/api/auth/register`
   - Body (JSON):
   ```json
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "TestPass123",
     "first_name": "Test",
     "last_name": "User"
   }
   ```

3. **Login:**
   - Method: POST
   - URL: `http://localhost:5000/api/auth/login`
   - Body (JSON):
   ```json
   {
     "username": "testuser",
     "password": "TestPass123"
   }
   ```
   - Copy the `access_token` from response

4. **Get current user:**
   - Method: GET
   - URL: `http://localhost:5000/api/auth/me`
   - Headers:
     - Key: `Authorization`
     - Value: `Bearer YOUR_ACCESS_TOKEN`

## Error Response Format

All error responses follow this format:
```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

## Next Steps

1. **Install dependencies:**
   ```bash
   pip install Flask-JWT-Extended Flask-Bcrypt email-validator
   ```

2. **Run database migrations:**
   ```bash
   flask db upgrade
   ```

3. **Start the Flask server:**
   ```bash
   python app.py
   ```

4. **Test the authentication endpoints** using Postman, cURL, or your Angular frontend.
