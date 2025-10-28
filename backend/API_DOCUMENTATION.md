# Header Configuration API Documentation

## Overview
The Header Configuration API provides comprehensive endpoints for managing dynamic table column configurations in the Credit Bill Tracker application. This API allows the frontend to dynamically show/hide columns, adjust their display order, and save user preferences.

## Base URL
```
http://localhost:5000/api
```

## Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/header-config` | Get all header configurations |
| GET | `/header-config/bills-with-config` | Get bills with header config (main endpoint) |
| GET | `/header-config/column/{colName}` | Get specific column configuration |
| PATCH | `/header-config/toggle-visibility/{colName}` | Toggle column visibility |
| PUT | `/header-config/bulk-update` | Bulk update configurations |
| POST | `/header-config/reset-defaults` | Reset all configs to defaults |
| PATCH | `/header-config/display-order` | Update column display order |

## Detailed Endpoints

### 1. Get All Header Configurations
```
GET /api/header-config
```

**Query Parameters:**
- `visible_only` (boolean, optional): If true, returns only visible columns

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "colName": "sNo",
      "label": "S.No",
      "status": true,
      "dataType": "number",
      "width": 80,
      "sortable": true,
      "searchable": true,
      "filterType": "text",
      "displayOrder": 1,
      "multiSelectFilter": [],
      "formatOptions": null
    }
  ],
  "count": 42
}
```

### 2. Get Bills with Header Configuration (Main Endpoint)
```
GET /api/header-config/bills-with-config
```

**Query Parameters:**
- `page` (integer, default: 1): Page number for pagination
- `per_page` (integer, default: 25, max: 100): Items per page
- `search` (string, optional): Global search term
- `status` (string, optional): Filter by status

**Response:**
```json
{
  "success": true,
  "data": {
    "bills": [
      {
        "id": 1,
        "sNo": 1,
        "cardNo": "1234****5678",
        "cumName": "HDFC Bank",
        "bankName": "HDFC Bank",
        "cardNumber": "1234****5678",
        "totalAmount": 50000.00,
        "minimumAmount": 2500.00,
        "status": "pending",
        "createdAt": "2024-10-19T10:30:00Z"
      }
    ],
    "headerConfig": [
      {
        "id": 1,
        "colName": "sNo",
        "label": "S.No",
        "status": true,
        "displayOrder": 1
      }
    ],
    "visibleColumns": ["sNo", "cardNo", "cumName"],
    "pagination": {
      "page": 1,
      "perPage": 25,
      "total": 150,
      "totalPages": 6,
      "hasNext": true,
      "hasPrev": false
    }
  }
}
```

### 3. Get Specific Column Configuration
```
GET /api/header-config/column/{colName}
```

**Parameters:**
- `colName` (string): Column name (e.g., "sNo", "cardNo")

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "colName": "sNo",
    "label": "S.No",
    "status": true,
    "dataType": "number",
    "width": 80,
    "sortable": true,
    "searchable": true,
    "filterType": "text",
    "displayOrder": 1
  }
}
```

### 4. Toggle Column Visibility
```
PATCH /api/header-config/toggle-visibility/{colName}
```

**Parameters:**
- `colName` (string): Column name

**Request Body:**
```json
{
  "visible": true  // Optional: set specific value, otherwise toggles
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "colName": "sNo",
    "status": true
  },
  "message": "Visibility toggled for column: sNo"
}
```

### 5. Bulk Update Configurations
```
PUT /api/header-config/bulk-update
```

**Request Body:**
```json
{
  "configs": [
    {
      "id": 1,
      "status": true,
      "width": 100,
      "displayOrder": 1
    },
    {
      "id": 2,
      "status": false,
      "width": 150
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "colName": "sNo",
      "status": true,
      "width": 100
    }
  ],
  "message": "Updated 2 configurations"
}
```

### 6. Reset to Defaults
```
POST /api/header-config/reset-defaults
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "status": true
    }
  ],
  "message": "Header configurations reset to defaults successfully"
}
```

### 7. Update Display Order
```
PATCH /api/header-config/display-order
```

**Request Body:**
```json
{
  "columnOrders": [
    {
      "colName": "sNo",
      "displayOrder": 1
    },
    {
      "colName": "cardNo", 
      "displayOrder": 2
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Display order updated successfully"
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error category",
  "message": "Detailed error description"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (missing parameters, invalid data)
- `404` - Not Found (column/configuration not found)
- `500` - Internal Server Error

## Frontend Integration

### Angular Service Usage

```typescript
// Get bills with configuration
this.headerConfigService.getBillsWithConfig({
  page: 1,
  perPage: 25,
  search: 'HDFC',
  status: 'pending'
}).subscribe(response => {
  this.bills = response.data.bills;
  this.headerConfigs = response.data.headerConfig;
  this.visibleColumns = response.data.visibleColumns;
});

// Toggle column visibility
this.headerConfigService.toggleColumnVisibility('sNo', true)
  .subscribe(response => {
    console.log('Column visibility updated');
  });

// Bulk update configurations
const updates = [
  { id: 1, status: true },
  { id: 2, status: false }
];
this.headerConfigService.bulkUpdateConfigs(updates)
  .subscribe(response => {
    console.log('Configurations updated');
  });
```

## Database Schema

### HeaderConfig Table
```sql
CREATE TABLE header_config (
    id SERIAL PRIMARY KEY,
    col_name VARCHAR(50) UNIQUE NOT NULL,
    label VARCHAR(100) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    data_type VARCHAR(20) DEFAULT 'text',
    width INTEGER DEFAULT 150,
    sortable BOOLEAN DEFAULT TRUE,
    searchable BOOLEAN DEFAULT TRUE,
    filter_type VARCHAR(20) DEFAULT 'text',
    display_order INTEGER DEFAULT 0,
    multi_select_filter TEXT,
    format_options TEXT,
    created_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Testing

Run the API test script:
```bash
cd backend
python test_header_api.py
```

Seed sample data:
```bash
cd backend
python seed_sample_data.py
```

## Security Considerations

1. **Input Validation**: All endpoints validate input parameters
2. **SQL Injection Prevention**: Using SQLAlchemy ORM with parameterized queries
3. **CORS**: Configured for Angular frontend (http://localhost:4200)
4. **Rate Limiting**: Consider implementing for production use

## Performance Notes

1. **Pagination**: Bills endpoint supports pagination to handle large datasets
2. **Indexing**: Database indexes on frequently queried columns
3. **Caching**: Consider implementing Redis caching for header configurations
4. **Batch Operations**: Bulk update endpoint for efficient multiple updates

## Future Enhancements

1. **User-specific configurations**: Save per-user column preferences
2. **Column grouping**: Group related columns together
3. **Advanced filtering**: Date ranges, multi-select filters
4. **Export configurations**: Import/export column settings
5. **Audit trail**: Track configuration changes over time