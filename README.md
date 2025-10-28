# Credit Bills Management System 🚀

A comprehensive full-stack application for managing credit card bills with dynamic table configuration and advanced filtering capabilities.

## 🏗️ Monorepo Structure

```
credit-bills-system/
├── backend/              # Flask API Server
│   ├── app/
│   │   ├── models/       # SQLAlchemy Models  
│   │   ├── routes/       # API Endpoints
│   │   └── __init__.py   # Flask App Factory
│   ├── config/           # Configuration Files
│   ├── migrations/       # Database Migrations
│   ├── requirements.txt  # Python Dependencies
│   └── run.py           # Application Entry Point
├── frontend/            # Angular Application
│   ├── src/
│   │   ├── app/         # Angular Components & Services
│   │   ├── environments/ # Environment Configurations
│   │   └── index.html   # Main HTML Template
│   ├── package.json     # Node.js Dependencies
│   ├── angular.json     # Angular CLI Configuration
│   └── tsconfig.json    # TypeScript Configuration  
├── docs/                # Project Documentation
├── scripts/             # Setup & Deployment Scripts
├── .gitignore           # Git Ignore Rules
└── README.md           # This File
```

## 🚀 Features

### Backend (Flask API)
- **Dynamic Column Configuration**: Manage table columns via `header_config` table
- **Credit Bills Management**: Full CRUD operations for credit bills
- **Advanced Filtering**: Search, pagination, and status filtering
- **RESTful API**: Well-documented API endpoints
- **Database Migrations**: Alembic for schema management

### Frontend (Angular)
- **Dynamic Table Rendering**: Columns configured from backend API
- **Real-time Search**: Global search across all searchable fields
- **Pagination**: Efficient data loading with pagination
- **Responsive Design**: Mobile-friendly interface
- **API Integration**: Seamless backend communication

## 🛠️ Tech Stack

**Backend:**
- Flask 2.x
- SQLAlchemy ORM
- Alembic (migrations)
- Python 3.8+

**Frontend:**
- Angular 20.x
- TypeScript
- RxJS
- HTML5/CSS3

**Database:**
- SQLite (development)
- PostgreSQL (production ready)

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 18+**
- **Git**

## 🚦 Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python init_db.py
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📖 API Documentation

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/header-config/bills-with-config` | Get bills with column config |
| GET | `/api/header-config` | Get all column configurations |
| PATCH | `/api/header-config/toggle-visibility/{colName}` | Toggle column visibility |
| PUT | `/api/header-config/bulk-update` | Bulk update configurations |

### Example Response
```json
{
  "success": true,
  "data": {
    "bills": [...],
    "headerConfig": [...],
    "visibleColumns": [...],
    "pagination": {...}
  }
}
```

## 🎯 Key Features

### Dynamic Table Configuration
- **42+ Configurable Columns**: All credit bill fields can be shown/hidden
- **Custom Labels**: Admin-friendly column names
- **Display Order**: Drag-and-drop column ordering
- **Width Control**: Pixel-perfect column widths
- **Filter Types**: Text, select, number, and date filters

### Advanced Search & Filtering
- **Global Search**: Search across multiple fields simultaneously
- **Status Filtering**: Filter by PAID, PENDING, OVERDUE status
- **Pagination**: Efficient loading with customizable page sizes
- **Sortable Columns**: Click-to-sort functionality

### Data Management
- **Real Credit Bill Data**: Complete credit card bill information
- **Mobile Numbers**: Customer contact information
- **Payment Status**: Track payment states
- **Bank Integration**: Multi-bank support
- **Amount Formatting**: Currency formatting (₹ INR)

## 🔧 Configuration

### Backend Configuration
```python
# config/config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///credit_bills.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Frontend Configuration
```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5000/api'
};
```

## 📊 Database Schema

### Credit Bills Table (42+ columns)
- Basic info: `s_no`, `card_no`, `cum_name`, `card_limit`
- Financial: `tad`, `norm`, `rb`, `emi`, `principle`
- Contact: `mobile`, `new_numbers`, `add1`, `add2`
- Status: `status`, `paid_unpaid`, `contact_status`
- Dates: `ptp_date`, `paid_date`, `created_at`

### Header Config Table
- Column metadata: `col_name`, `label`, `status`
- Display settings: `width`, `display_order`
- Filter settings: `filter_type`, `multi_select_filter`

## 🚀 Deployment

### Production Setup
1. **Backend**: Use Gunicorn + Nginx
2. **Frontend**: Build with `ng build --prod`
3. **Database**: PostgreSQL for production
4. **Environment**: Docker containers recommended

### Environment Variables
```bash
# Backend
FLASK_ENV=production
DATABASE_URL=postgresql://...

# Frontend
NG_APP_API_URL=https://api.yourdomain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Issues & Support

- **Bug Reports**: Use GitHub Issues
- **Feature Requests**: Use GitHub Issues with `enhancement` label
- **Questions**: Use GitHub Discussions

## 🔄 Version History

- **v1.0.0** - Initial release with dynamic table and API integration
- **v0.9.0** - Beta release with basic functionality
- **v0.1.0** - Project setup and structure

## 📞 Contact

- **Developer**: Credit Bills Team
- **Email**: developer@creditbills.com
- **Project**: [GitHub Repository](https://github.com/your-org/credit-bills-system)