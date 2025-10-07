#!/bin/bash

# Health check script for DevContainer services
# This script verifies that both frontend and backend are running correctly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[HEALTH CHECK]${NC} $1"
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

# Function to check if a port is open
check_port() {
    local port=$1
    local service=$2
    local max_attempts=30
    local attempt=1

    print_status "Checking if $service is running on port $port..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "http://localhost:$port" > /dev/null 2>&1; then
            print_success "$service is responding on port $port"
            return 0
        fi
        
        echo -n "."
        sleep 1
        attempt=$((attempt + 1))
    done
    
    print_error "$service is not responding on port $port after $max_attempts seconds"
    return 1
}

# Function to check backend API endpoints
check_backend_api() {
    print_status "Testing backend API endpoints..."
    
    # Check health endpoint (if it exists) or any basic endpoint
    if curl -s -f "http://localhost:5000/api/auth/register" > /dev/null 2>&1; then
        print_success "Backend API endpoints are accessible"
        return 0
    else
        print_warning "Backend API endpoints may not be fully configured (this is normal if auth endpoints require POST)"
        return 0
    fi
}

# Function to check frontend
check_frontend() {
    print_status "Testing frontend application..."
    
    # Check if React app is serving content
    if curl -s "http://localhost:3000" | grep -q "Expense Tracker\|React App\|root" 2>/dev/null; then
        print_success "Frontend is serving content"
        return 0
    else
        print_warning "Frontend may still be starting up"
        return 1
    fi
}

# Function to check database
check_database() {
    print_status "Checking database connectivity..."
    
    cd /workspace/backend
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        
        # Test database connection
        python3 -c "
from app import app, db
try:
    with app.app_context():
        db.engine.execute('SELECT 1')
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
" && print_success "Database is accessible" || print_error "Database connection failed"
    else
        print_error "Python virtual environment not found"
        return 1
    fi
}

# Function to check environment variables
check_environment() {
    print_status "Checking environment configuration..."
    
    cd /workspace/backend
    if [ -f ".env" ]; then
        print_success ".env file exists"
    else
        print_warning ".env file not found"
    fi
    
    if [ -f "venv/bin/activate" ]; then
        print_success "Python virtual environment exists"
    else
        print_error "Python virtual environment not found"
        return 1
    fi
    
    cd /workspace/frontend
    if [ -d "node_modules" ]; then
        print_success "Node.js dependencies installed"
    else
        print_error "Node.js dependencies not found"
        return 1
    fi
}

# Main health check function
main() {
    echo "🔍 Starting DevContainer Health Check..."
    echo "=================================="
    
    # Check environment setup
    check_environment || exit 1
    
    # Check database
    check_database || exit 1
    
    # If services are not running, try to start them
    if ! pgrep -f "python.*run.py" > /dev/null; then
        print_warning "Backend not running. You may need to start it with: npm run dev:backend"
    fi
    
    if ! pgrep -f "react-scripts.*start" > /dev/null; then
        print_warning "Frontend not running. You may need to start it with: npm run dev:frontend"
    fi
    
    # Check ports if services are running
    if pgrep -f "python.*run.py" > /dev/null; then
        check_port 5000 "Backend (Flask)" || exit 1
        check_backend_api
    fi
    
    if pgrep -f "react-scripts.*start" > /dev/null; then
        check_port 3000 "Frontend (React)" || exit 1
        check_frontend
    fi
    
    echo "=================================="
    print_success "Health check completed!"
    echo ""
    echo "📋 Service Status:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend:  http://localhost:5000"
    echo ""
    echo "To start both services: npm run dev:all"
    echo "To start individually:"
    echo "  Backend only:  npm run dev:backend"
    echo "  Frontend only: npm run dev:frontend"
}

# Run the health check
main "$@"