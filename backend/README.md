# DueMatrix Backend API

Flask-based REST API with PostgreSQL database using SQLAlchemy ORM and MVC architecture.

## Project Structure

```
backend/
├── app.py                  # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── models/               # Database models (M in MVC)
│   ├── __init__.py
│   └── header_model.py   # ColumnHeader model
├── controllers/          # Route handlers (C in MVC)
│   ├── __init__.py
│   └── header_controller.py
└── migrations/           # Database migrations (auto-generated)
```

## Setup Instructions

### 1. Create Virtual Environment

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Database Setup

Make sure PostgreSQL is running and create the database:

```sql
CREATE DATABASE duematrix;
```

### 4. Initialize Database Migrations

```powershell
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run the Application

```powershell
python app.py
```

Or use Flask CLI:

```powershell
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Column Headers API

#### Get All Headers
```
GET /api/headers
```

#### Get Single Header
```
GET /api/headers/<id>
```

#### Create Header
```
POST /api/headers
Content-Type: application/json

{
  "col_header": "customer_name",
  "col_label": "Customer Name",
  "is_editable": true,
  "is_multi_select": false,
  "col_width": 12.5,
  "display": true,
  "default_display": true,
  "is_frozen": true,
  "display_order": 1
}
```

#### Update Header
```
PUT /api/headers/<id>
Content-Type: application/json

{
  "col_label": "Updated Label",
  "is_frozen": false
}
```

#### Delete Header
```
DELETE /api/headers/<id>
```

#### Bulk Create Headers
```
POST /api/headers/bulk
Content-Type: application/json

[
  {
    "col_header": "id",
    "col_label": "ID",
    ...
  },
  {
    "col_header": "name",
    "col_label": "Name",
    ...
  }
]
```

#### Get Default Headers
```
GET /api/headers/default
```

## Environment Variables

Configuration is managed through `.env` file:

```env
# Database
DB_TYPE=postgresql
DB_USERNAME=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432
DB_NAME=duematrix

# Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key

# CORS
CORS_ORIGINS=http://localhost:4200
```

## Database Schema

### column_headers Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| col_header | String(100) | Unique column identifier |
| col_label | String(200) | Display label |
| is_editable | Boolean | Can be edited |
| is_multi_select | Boolean | Multi-select filter |
| col_width | Float | Width in rem |
| display | Boolean | Show in table |
| default_display | Boolean | Show by default |
| is_frozen | Boolean | Freeze column |
| display_order | Integer | Display order |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Update timestamp |
| created_by | String(100) | Creator |
| updated_by | String(100) | Last updater |

## Development

### Running Tests
```powershell
# TODO: Add tests
```

### Database Migrations

After model changes:
```powershell
flask db migrate -m "Description of changes"
flask db upgrade
```

To rollback:
```powershell
flask db downgrade
```

## Technologies Used

- **Flask 3.0.0** - Web framework
- **SQLAlchemy 3.1.1** - ORM
- **PostgreSQL** - Database
- **Flask-CORS** - CORS support
- **Flask-Migrate** - Database migrations
- **python-dotenv** - Environment variables
