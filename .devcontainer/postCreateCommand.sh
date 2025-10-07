#!/bin/bash

# Exit on any error
set -e

echo "🚀 Setting up Expense Tracker DevContainer..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Ensure we're in the workspace directory
cd /workspace

print_status "Setting up Python virtual environment for backend..."

# Create Python virtual environment for backend
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Created Python virtual environment"
else
    print_warning "Python virtual environment already exists"
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Python dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file from .env.example..."
    cp .env.example .env
    print_success ".env file created"
else
    print_warning ".env file already exists"
fi

# Initialize database
print_status "Initializing SQLite database..."
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created successfully')
"
print_success "Database initialized"

# Deactivate virtual environment
deactivate

# Navigate to frontend directory
cd ../frontend

print_status "Installing Node.js dependencies for frontend..."

# Install Node.js dependencies
npm install
print_success "Node.js dependencies installed"

# Navigate back to workspace root
cd ..

# Create development scripts
print_status "Creating development scripts..."

# Create start-backend script
cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
echo "🐍 Starting Flask backend on http://localhost:5000"
python run.py
EOF
chmod +x start-backend.sh

# Create start-frontend script
cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
echo "⚛️  Starting React frontend on http://localhost:3000"
npm start
EOF
chmod +x start-frontend.sh

# Create start-all script using concurrently
cat > start-all.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting both frontend and backend services..."
npx concurrently \
  --names "BACKEND,FRONTEND" \
  --prefix-colors "blue,green" \
  "cd backend && source venv/bin/activate && python run.py" \
  "cd frontend && npm start"
EOF
chmod +x start-all.sh

print_success "Development scripts created"

# Add npm scripts to package.json in workspace root
print_status "Adding convenience npm scripts..."
cat > package.json << 'EOF'
{
  "name": "expense-tracker-devcontainer",
  "version": "1.0.0",
  "description": "DevContainer setup for Expense Tracker",
  "scripts": {
    "dev:backend": "./start-backend.sh",
    "dev:frontend": "./start-frontend.sh",
    "dev:all": "./start-all.sh",
    "test:backend": "cd backend && source venv/bin/activate && python -m pytest",
    "test:frontend": "cd frontend && npm test",
    "build:frontend": "cd frontend && npm run build",
    "lint:backend": "cd backend && source venv/bin/activate && flake8 .",
    "lint:frontend": "cd frontend && npm run lint",
    "format:backend": "cd backend && source venv/bin/activate && black . && isort .",
    "install:backend": "cd backend && source venv/bin/activate && pip install -r requirements.txt",
    "install:frontend": "cd frontend && npm install"
  },
  "devDependencies": {
    "concurrently": "^7.6.0"
  }
}
EOF

# Install concurrently for running both services
npm install

print_success "Setup completed successfully!"

echo ""
echo "🎉 DevContainer is ready!"
echo ""
echo "Available commands:"
echo "  npm run dev:all      - Start both frontend and backend"
echo "  npm run dev:backend  - Start only backend (Flask)"
echo "  npm run dev:frontend - Start only frontend (React)"
echo "  npm run test:backend - Run backend tests"
echo "  npm run test:frontend- Run frontend tests"
echo ""
echo "Services will be available at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:5000"
echo ""
print_success "Happy coding! 🚀"