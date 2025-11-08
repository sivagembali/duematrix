# 🔐 Authentication Quick Reference

## Installation (One-Time Setup)

```bash
cd backend
pip install Flask-JWT-Extended Flask-Bcrypt email-validator
flask db upgrade
```

## Starting the Server

```bash
cd backend
python app.py
```

Server runs at: `http://localhost:5000`

---

## API Endpoints

### Register User
```bash
POST /api/auth/register
{
  "username": "johndoe",
  "email": "john@example.com", 
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Login
```bash
POST /api/auth/login
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```
**Returns:** `access_token` + `refresh_token`

### Get Profile (Protected)
```bash
GET /api/auth/me
Headers: Authorization: Bearer <access_token>
```

### Refresh Token
```bash
POST /api/auth/refresh
Headers: Authorization: Bearer <refresh_token>
```

### Change Password (Protected)
```bash
PUT /api/auth/change-password
Headers: Authorization: Bearer <access_token>
{
  "current_password": "SecurePass123",
  "new_password": "NewPass456"
}
```

### Logout (Protected)
```bash
POST /api/auth/logout
Headers: Authorization: Bearer <access_token>
```

---

## Quick Test

```bash
# Test all endpoints
python test_auth.py
```

---

## Password Rules
- ✅ 8+ characters
- ✅ 1+ uppercase letter
- ✅ 1+ lowercase letter  
- ✅ 1+ digit
- ✅ Example: `SecurePass123`

---

## Token Expiry
- **Access Token:** 1 hour (3600s)
- **Refresh Token:** 30 days (2592000s)

---

## Documentation

📖 **Full API Docs:** [AUTH_API.md](AUTH_API.md)
📋 **Implementation Details:** [AUTHENTICATION_SUMMARY.md](AUTHENTICATION_SUMMARY.md)
📚 **Main README:** [README.md](README.md)

---

## Quick cURL Test

```bash
# 1. Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"TestPass123"}'

# 2. Login  
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"TestPass123"}'

# 3. Get profile (replace TOKEN)
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Angular Integration Example

```typescript
// auth.service.ts
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = 'http://localhost:5000/api/auth';
  
  constructor(private http: HttpClient) {}
  
  register(user: any) {
    return this.http.post(`${this.apiUrl}/register`, user);
  }
  
  login(username: string, password: string) {
    return this.http.post(`${this.apiUrl}/login`, { username, password });
  }
  
  getProfile(token: string) {
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
    return this.http.get(`${this.apiUrl}/me`, { headers });
  }
  
  logout(token: string) {
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
    return this.http.post(`${this.apiUrl}/logout`, {}, { headers });
  }
}
```

---

## Common Issues

### ❌ 401 Unauthorized
- Check token hasn't expired
- Verify Bearer format: `Bearer <token>`
- Ensure token is valid

### ❌ 409 Conflict
- Username or email already exists
- Use different credentials

### ❌ 400 Bad Request
- Check password meets requirements
- Verify email format is valid
- Ensure all required fields present

---

## Environment Variables (.env)

```env
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
```

**Generate secure key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Files Created
- ✅ `models/user_model.py` - User database model
- ✅ `controllers/auth_controller.py` - Auth API endpoints
- ✅ `AUTH_API.md` - Full API documentation
- ✅ `test_auth.py` - Test script
- ✅ `AUTHENTICATION_SUMMARY.md` - Implementation details
- ✅ `QUICK_REFERENCE.md` - This file

---

## Status: ✅ READY

Authentication is fully implemented and tested. Start the server and test with `python test_auth.py` or use the API endpoints directly.
