# Expense Tracker Backend

A Flask-based REST API for managing personal expenses with user authentication and CRUD operations.

## Features

- 🔐 JWT-based authentication
- 👤 User registration and login
- 💰 Expense management (CRUD operations)
- 📊 Expense categorization and filtering
- 🔍 Pagination and search capabilities
- 📱 CORS support for frontend integration
- 🛡️ Input validation and error handling

## Technology Stack

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite** - Database (development)
- **Werkzeug** - Password hashing

## Project Structure

```
backend/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── models.py           # Database models
├── auth.py             # Authentication utilities
├── routes/
│   ├── __init__.py
│   ├── auth.py         # Authentication routes
│   └── expenses.py     # Expense management routes
├── requirements.txt    # Python dependencies
├── run.py              # Application runner
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Initialize Database

```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### 4. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | User login | No |
| POST | `/api/auth/logout` | User logout | Yes |
| GET | `/api/auth/me` | Get current user | Yes |

### Expenses

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/expenses` | Get user expenses | Yes |
| POST | `/api/expenses` | Create new expense | Yes |
| GET | `/api/expenses/<id>` | Get specific expense | Yes |
| PUT | `/api/expenses/<id>` | Update expense | Yes |
| DELETE | `/api/expenses/<id>` | Delete expense | Yes |
| GET | `/api/expenses/categories` | Get available categories | No |

### User Profile

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/user/profile` | Get user profile | Yes |
| PUT | `/api/user/profile` | Update user profile | Yes |

## Request/Response Examples

### User Registration

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### User Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### Create Expense

```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "amount": 25.50,
    "description": "Lunch at cafe",
    "category": "Food",
    "date": "2024-01-15"
  }'
```

### Get Expenses with Filtering

```bash
curl "http://localhost:5000/api/expenses?category=Food&date_from=2024-01-01&page=1&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `password_hash` - Hashed password
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Expenses Table
- `id` - Primary key
- `user_id` - Foreign key to users table
- `amount` - Expense amount (decimal)
- `description` - Expense description
- `category` - Expense category
- `date` - Expense date
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## Available Categories

- Food
- Transportation
- Entertainment
- Healthcare
- Shopping
- Utilities
- Other

## Environment Variables

Create a `.env` file with the following variables:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///expense_tracker.db
CORS_ORIGINS=http://localhost:3000
```

## CLI Commands

### Initialize Database
```bash
flask init-db
```

### Seed Database with Sample Data
```bash
flask seed-db
```

## Error Handling

The API returns consistent error responses:

```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

## Security Features

- Password hashing with Werkzeug
- JWT token authentication
- Token blacklisting on logout
- Input validation and sanitization
- CORS configuration
- SQL injection prevention via SQLAlchemy ORM

## Testing the API

You can test the API using tools like:
- **Postman** - GUI-based API testing
- **curl** - Command-line testing
- **HTTPie** - User-friendly command-line HTTP client

Example with HTTPie:
```bash
http POST localhost:5000/api/auth/register username=testuser email=test@example.com password=password123
```

## Development Notes

- The application uses SQLite for development (no additional setup required)
- JWT tokens expire after 1 hour by default
- The API supports pagination with `page` and `limit` parameters
- All timestamps are in UTC
- Decimal amounts are stored with 2 decimal places precision

## Production Deployment

For production deployment:

1. Change `FLASK_ENV=production` in your environment
2. Use a production database (PostgreSQL recommended)
3. Set strong secret keys
4. Configure proper CORS origins
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Set up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.