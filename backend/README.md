# Credit Bill Tracker - Backend API

Flask-based REST API for managing credit bill payment tracking with PostgreSQL database.

## 🚀 Quick Setup

### Prerequisites
- Python 3.8+ installed
- PostgreSQL 12+ installed and running
- Git (optional)

### 1. Environment Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

1. **Create PostgreSQL Database:**
```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database
CREATE DATABASE credit_bill_tracker;

-- Create user (optional)
CREATE USER credit_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE credit_bill_tracker TO credit_user;
```

2. **Configure Environment Variables:**
```bash
# Copy example environment file
copy .env.example .env

# Edit .env file with your database credentials:
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=credit_bill_tracker
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### 3. Initialize Database

```bash
# Create tables and insert sample data
python init_db.py
```

### 4. Run the Application

```bash
# Start Flask development server
python run.py
```

The API will be available at: `http://localhost:5000`

## 📋 API Endpoints

### Bills Management
- `GET /api/bills` - Get all bills (with pagination, search, filtering)
- `GET /api/bills/{id}` - Get specific bill by ID
- `POST /api/bills` - Create new bill
- `PUT /api/bills/{id}` - Update existing bill
- `DELETE /api/bills/{id}` - Delete bill

### Statistics
- `GET /api/bills/stats` - Get bills statistics

### Health Check
- `GET /health` - API health status

## 🔧 API Usage Examples

### Get All Bills
```bash
GET http://localhost:5000/api/bills?page=1&per_page=10&search=Rajesh&status=UNPAID
```

### Create New Bill
```bash
POST http://localhost:5000/api/bills
Content-Type: application/json

{
  "sNo": 6,
  "cardNo": "1111-2222-3333-4444",
  "cumName": "New Customer",
  "cardLimit": 50000.00,
  "mobile": "9999888877",
  "paidUnpaid": "UNPAID"
}
```

### Update Bill
```bash
PUT http://localhost:5000/api/bills/1
Content-Type: application/json

{
  "paidUnpaid": "PAID",
  "paidAmount": 15000.00,
  "paidDate": "2025-10-18"
}
```

## 🗃️ Database Schema

The `credit_bills` table includes all 42 columns from your frontend:
- Basic Info: S/NO, CARD NO, CUM NAME, CARD LIMIT
- Financial: TOS, POS, TAD, NORM, RB, EMI, PRINCIPLE, etc.
- Contact: MOBILE, NEW NUMBERS, addresses
- Status: PAID/UNPAID, STATUS, BLOCK, CYCLE
- Management: EMP NAME, MANAGER, AREAS, MIS
- Tracking: PTP DATE, PAID DATE, REMARKS, HISTORY

## 🔐 Security Features

- CORS configured for Angular frontend
- PostgreSQL parameterized queries (SQL injection protection)
- Environment-based configuration
- Error handling and validation

## 📈 Features

- **Pagination**: Efficient data loading for large datasets
- **Search**: Search by customer name, card number, or mobile
- **Filtering**: Filter by payment status, block status, etc.
- **Statistics**: Summary dashboard data
- **Audit Trail**: Created/updated timestamps
- **Error Handling**: Comprehensive error responses

## 🔧 Development

### Project Structure
```
backend/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   └── __init__.py      # App factory
├── config/
│   └── config.py        # Configuration classes
├── requirements.txt     # Python dependencies
├── run.py              # Application entry point
├── init_db.py          # Database initialization
└── .env                # Environment variables
```

### Adding New Features

1. **New Model**: Add to `app/models/`
2. **New Routes**: Add to `app/routes/`
3. **Configuration**: Update `config/config.py`
4. **Dependencies**: Add to `requirements.txt`

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check PostgreSQL is running
   - Verify credentials in `.env`
   - Ensure database exists

2. **Import Errors**
   - Activate virtual environment
   - Install requirements: `pip install -r requirements.txt`

3. **CORS Errors**
   - Check Angular app runs on `localhost:4200`
   - CORS is configured for this origin

### Logs
Check console output for detailed error messages and API request logs.

## 🔄 Frontend Integration

Update your Angular service to use these endpoints:
- Base URL: `http://localhost:5000/api`
- All endpoints return JSON with `success`, `data`, and optional `message` fields
- Pagination info included in `/bills` responses