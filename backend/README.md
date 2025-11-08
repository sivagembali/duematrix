# DueMatrix Backend API

Flask-based REST API with PostgreSQL database, JWT authentication, SQLAlchemy ORM, and MVC architecture.

## Features

- ✅ RESTful API with Flask
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ JWT-based authentication with Flask-JWT-Extended
- ✅ Password hashing with bcrypt
- ✅ Database migrations with Flask-Migrate
- ✅ CORS support for Angular frontend
- ✅ MVC architecture pattern
- ✅ User authentication and authorization
- ✅ Column header configuration management

## Project Structure

```
backend/
├── app.py                      # Application entry point with JWT & Bcrypt
├── config.py                   # Configuration settings with JWT config
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── AUTH_API.md                # Authentication API documentation
├── models/                    # Database models (M in MVC)
│   ├── __init__.py
│   ├── user_model.py          # User model for authentication
│   └── header_model.py        # ColumnHeader model
├── controllers/               # Route handlers (C in MVC)
│   ├── __init__.py
│   ├── auth_controller.py     # Authentication endpoints
│   └── header_controller.py   # Column header endpoints
└── migrations/                # Database migrations (auto-generated)
```

## Tech Stack

- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM
- **Flask-JWT-Extended 4.6.0** - JWT authentication
- **Flask-Bcrypt 1.0.1** - Password hashing
- **Flask-CORS 4.0.0** - Cross-origin support
- **Flask-Migrate 4.0.5** - Database migrations
- **PostgreSQL** - Database
- **psycopg2-binary 2.9.7** - PostgreSQL adapter

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

### 4. Environment Configuration

The `.env` file should contain:

```env
# Database Configuration
DB_TYPE=postgresql
DB_USERNAME=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432
DB_NAME=duematrix

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# CORS Configuration
CORS_ORIGINS=http://localhost:4200
```

**Important:** Change `SECRET_KEY` and `JWT_SECRET_KEY` in production!

### 5. Initialize Database Migrations

```powershell
flask db migrate -m "Initial migration with User model"
flask db upgrade
```

### 6. Run the Application

```powershell
python app.py
```

Or use Flask CLI:

```powershell
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication APIs (`/api/auth`)

📖 **See [AUTH_API.md](AUTH_API.md) for detailed authentication documentation**

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user  
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user (requires JWT)
- `PUT /api/auth/change-password` - Change password (requires JWT)
- `POST /api/auth/logout` - Logout user (requires JWT)

### Column Headers API (`/api`)

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
