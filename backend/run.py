#!/usr/bin/env python3
"""
Expense Tracker Backend Application Runner

This script runs the Flask application for the Expense Tracker backend.
It handles database initialization and starts the development server.
"""

import os
from app import create_app, db

def main():
    """Main function to run the application."""
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create the Flask app
    app = create_app()
    
    # Initialize database
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database initialized successfully!")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            return
    
    # Start the development server
    print("🚀 Starting Expense Tracker Backend...")
    print("📍 Server running at: http://localhost:5000")
    print("📋 API Documentation available at: http://localhost:5000")
    print("🔧 Environment: development")
    print("💾 Database: SQLite (expense_tracker.db)")
    print("\n📖 Available endpoints:")
    print("   - POST /api/auth/register - Register new user")
    print("   - POST /api/auth/login - User login")
    print("   - POST /api/auth/logout - User logout")
    print("   - GET  /api/auth/me - Get current user")
    print("   - GET  /api/expenses - Get user expenses")
    print("   - POST /api/expenses - Create expense")
    print("   - GET  /api/expenses/<id> - Get specific expense")
    print("   - PUT  /api/expenses/<id> - Update expense")
    print("   - DELETE /api/expenses/<id> - Delete expense")
    print("   - GET  /api/expenses/categories - Get categories")
    print("   - GET  /api/user/profile - Get user profile")
    print("   - PUT  /api/user/profile - Update user profile")
    print("\n🛑 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")

if __name__ == '__main__':
    main()