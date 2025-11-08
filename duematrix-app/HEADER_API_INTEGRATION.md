# Header API Integration Flow

## Overview
The application now automatically fetches column headers from the backend API after successful login and makes them available throughout the application.

## Implementation Details

### 1. Login Flow with Header Fetching

**AuthService** (`auth.service.ts`):
```typescript
login(credentials: LoginRequest): Observable<LoginResponse> {
  return this.http.post<LoginResponse>(`${this.apiUrl}/login`, credentials).pipe(
    tap((response) => {
      if (response.success) {
        this.storeAuthData(response.data);
      }
    }),
    switchMap((response) => {
      if (response.success) {
        // Automatically fetch headers after successful login
        return this.headerService.getDashboardHeaders().pipe(
          tap((headerResponse) => {
            if (headerResponse.success) {
              this.headersSubject.next(headerResponse.data);
              localStorage.setItem('columnHeaders', JSON.stringify(headerResponse.data));
            }
          }),
          switchMap(() => of(response))
        );
      }
      return of(response);
    })
  );
}
```

### 2. Header Storage & Access

**Storage:**
- Headers are stored in `localStorage` as `columnHeaders`
- Headers are also stored in `BehaviorSubject` for reactive access
- Cleared on logout

**Access:**
```typescript
// Via Observable (reactive)
authService.headers$.subscribe(headers => {
  console.log('Headers updated:', headers);
});

// Direct access
const headers = authService.getHeadersValue();
```

### 3. MockDataGenerator Integration

**Updated** (`mock-data.service.ts`):
```typescript
static generateHeaderMapping(): ColumnHeader[] {
  // Try to get headers from auth service (loaded from API)
  const apiHeaders = this.authService.getHeadersValue();
  
  if (apiHeaders && apiHeaders.length > 0) {
    console.log('Using headers from API:', apiHeaders.length);
    return apiHeaders;
  }
  
  // Fallback to static headers if API headers not available
  console.warn('API headers not available, using fallback static headers');
  // ... fallback logic
}
```

### 4. Dashboard Display

**DashboardComponent** (`dashboard.ts`):
- Subscribes to `authService.headers$` observable
- Displays headers in a PrimeNG table
- Shows visual indicator that headers are loaded from API

## API Endpoints

### Get Dashboard Headers
```
GET /api/headers/dashboard
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "col_header": "id",
      "col_label": "ID",
      "is_editable": false,
      "is_multi_select": false,
      "col_width": 5,
      "display": true,
      "default_display": true,
      "is_frozen": true,
      "display_order": 1,
      "role_id": null,
      "created_at": "2025-11-08T20:35:19.976809Z",
      "updated_at": "2025-11-08T20:35:19.976812Z"
    },
    // ... 49 more headers
  ],
  "count": 50,
  "user": {
    "id": 1,
    "username": "admin_user",
    "role_id": 1
  }
}
```

## Benefits

1. **Dynamic Headers**: Headers are fetched from the database, allowing runtime configuration
2. **Role-Based Access**: API can filter headers based on user's role
3. **Cached**: Headers are stored in localStorage for offline access
4. **Reactive**: Components can subscribe to header changes
5. **Fallback**: Static headers available if API fails

## Testing

1. **Login**: Log in with valid credentials
2. **Check Console**: You should see: "Using headers from API: 50"
3. **Dashboard**: Navigate to dashboard to see headers displayed
4. **Logout**: Verify headers are cleared from localStorage
5. **Fallback**: Disable backend to test fallback headers

## Files Modified

- `duematrix-app/src/app/services/auth.service.ts` - Added header fetching on login
- `duematrix-app/src/app/services/mock-data.service.ts` - Integrated with AuthService
- `duematrix-app/src/app/components/dashboard/dashboard.ts` - Subscribe to headers
- `duematrix-app/src/app/components/dashboard/dashboard.html` - Display API badge
- `duematrix-app/src/app/components/dashboard/dashboard.scss` - Styled API badge

## Database

50 column headers are seeded in the database:
- Run: `python seed_comprehensive_headers.py`
- All headers available to all roles (role_id = NULL)
- Can be customized per role by updating role_id field
