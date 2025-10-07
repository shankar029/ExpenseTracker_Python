# DevContainer Setup for Expense Tracker

This DevContainer configuration provides a complete development environment for the Expense Tracker application with both React frontend and Flask backend.

## 🚀 Quick Start

1. **Prerequisites:**
   - Docker Desktop installed and running
   - Visual Studio Code with the "Dev Containers" extension

2. **Open in DevContainer:**
   - Open the project in VS Code
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Dev Containers: Reopen in Container"
   - Wait for the container to build and setup to complete

3. **Start Development:**
   ```bash
   # Start both frontend and backend
   npm run dev:all
   
   # Or start services individually
   npm run dev:backend   # Flask backend only
   npm run dev:frontend  # React frontend only
   ```

4. **Access the Application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 📁 DevContainer Structure

```
.devcontainer/
├── devcontainer.json       # Main DevContainer configuration
├── Dockerfile             # Custom Docker image
├── docker-compose.yml     # Multi-service orchestration
├── postCreateCommand.sh   # Automated setup script
└── README.md             # This file
```

## 🛠️ Available Commands

### Development
- `npm run dev:all` - Start both frontend and backend concurrently
- `npm run dev:backend` - Start Flask backend only
- `npm run dev:frontend` - Start React frontend only

### Testing
- `npm run test:backend` - Run Python tests with pytest
- `npm run test:frontend` - Run React tests with Jest

### Build
- `npm run build:frontend` - Build React app for production

### Code Quality
- `npm run lint:backend` - Lint Python code with flake8
- `npm run lint:frontend` - Lint React code with ESLint
- `npm run format:backend` - Format Python code with Black and isort

### Dependencies
- `npm run install:backend` - Install Python dependencies
- `npm run install:frontend` - Install Node.js dependencies

## 🔧 Features Included

### Development Tools
- **Python 3.11+** with virtual environment
- **Node.js 18+** with npm
- **Git** integration
- **SQLite3** database
- **Development utilities** (vim, curl, htop, tree, jq)

### VS Code Extensions
- Python development (Python, Black, isort, Pylint)
- React/JavaScript development (TypeScript, ESLint, Prettier)
- General development tools (Path IntelliSense, Auto Rename Tag)

### Port Forwarding
- Port 3000: React development server
- Port 5000: Flask API server

## 🐛 Troubleshooting

### Container Build Issues
```bash
# Rebuild container without cache
Ctrl+Shift+P → "Dev Containers: Rebuild Container"
```

### Python Environment Issues
```bash
# Recreate virtual environment
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Node.js Issues
```bash
# Clear npm cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database Issues
```bash
# Reinitialize database
cd backend
source venv/bin/activate
python3 -c "from app import app, db; app.app_context().push(); db.drop_all(); db.create_all()"
```

### Port Already in Use
```bash
# Kill processes on ports
sudo lsof -ti:3000 | xargs kill -9
sudo lsof -ti:5000 | xargs kill -9
```

## 🔐 Environment Configuration

The DevContainer automatically creates a `.env` file in the backend directory with development defaults:

```env
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production
DATABASE_URL=sqlite:///expense_tracker.db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

⚠️ **Important:** Change these values for production use!

## 📦 Development Workflow

1. **Code Changes:**
   - Backend: Hot reloading enabled with Flask development mode
   - Frontend: Hot reloading enabled with React development server

2. **Database Changes:**
   - SQLite database persists across container restarts
   - Located at `backend/expense_tracker.db`

3. **Testing:**
   - Backend tests: Run with `npm run test:backend`
   - Frontend tests: Run with `npm run test:frontend`

4. **Debugging:**
   - Python debugging configured for VS Code
   - JavaScript debugging available through browser dev tools

## 🚀 Production Deployment

This DevContainer is for development only. For production:

1. Use proper environment variables
2. Use a production database (PostgreSQL)
3. Build React app for production
4. Use a production WSGI server (Gunicorn)
5. Implement proper security measures

## 📝 Notes

- The container runs as the `vscode` user (UID 1000)
- Source code is mounted with cached consistency for better performance
- All development tools are pre-installed and configured
- Database is automatically initialized on first run

## 🆘 Getting Help

If you encounter issues:

1. Check the container logs in VS Code terminal
2. Verify Docker Desktop is running
3. Try rebuilding the container
4. Check this troubleshooting guide
5. Review the individual service logs

Happy coding! 🎉