import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from config import config
from models import db, User, Expense
from routes.auth import auth_bp
from routes.expenses import expenses_bp
from auth import is_token_blacklisted

def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initialize CORS - Allow all origins for development/testing
    # Note: When using credentials, we can't use "*" for origins, so we use a permissive function
    def cors_origin_handler(origin):
        # Allow all origins for development
        print(f"DEBUG: CORS origin check for: {origin}")
        return True
    
    # Add before_request handler to log all requests
    @app.before_request
    def log_request_info():
        from flask import request
        print(f"DEBUG: {request.method} {request.url}")
        print(f"DEBUG: Origin header: {request.headers.get('Origin')}")
        print(f"DEBUG: All headers: {dict(request.headers)}")
        
        # Handle preflight requests explicitly
        if request.method == 'OPTIONS':
            print("DEBUG: Handling OPTIONS preflight request")
            response = jsonify({'status': 'OK'})
            origin = request.headers.get('Origin')
            if origin:
                response.headers['Access-Control-Allow-Origin'] = origin
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response
    
    CORS(app,
         origins=cors_origin_handler,
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # JWT token blacklist checker
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_blacklisted(jwt_payload)
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"DEBUG: Invalid token error: {error}")
        print(f"DEBUG: JWT_SECRET_KEY being used: {app.config.get('JWT_SECRET_KEY', 'NOT_SET')}")
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is required'}), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has been revoked'}), 401
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'Expense Tracker API is running'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Welcome to Expense Tracker API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'expenses': '/api/expenses',
                'health': '/api/health'
            }
        }), 200
    
    # User profile endpoints
    @app.route('/api/user/profile', methods=['GET'])
    @jwt_required()
    def get_user_profile():
        """Get user profile information."""
        try:
            current_user_id = int(get_jwt_identity())
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({'user': user.to_dict()}), 200
            
        except Exception as e:
            return jsonify({'error': 'Failed to get user profile'}), 500
    
    @app.route('/api/user/profile', methods=['PUT'])
    @jwt_required()
    def update_user_profile():
        """Update user profile information."""
        from flask import request
        from auth import validate_email, validate_username
        
        try:
            current_user_id = int(get_jwt_identity())
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Update username if provided
            if 'username' in data:
                username = data['username'].strip()
                valid_username, username_message = validate_username(username)
                if not valid_username:
                    return jsonify({'error': username_message}), 400
                
                # Check if username already exists (excluding current user)
                existing_user = User.query.filter(
                    User.username == username,
                    User.id != current_user_id
                ).first()
                
                if existing_user:
                    return jsonify({'error': 'Username already exists'}), 409
                
                user.username = username
            
            # Update email if provided
            if 'email' in data:
                email = data['email'].strip().lower()
                valid_email, email_message = validate_email(email)
                if not valid_email:
                    return jsonify({'error': email_message}), 400
                
                # Check if email already exists (excluding current user)
                existing_user = User.query.filter(
                    User.email == email,
                    User.id != current_user_id
                ).first()
                
                if existing_user:
                    return jsonify({'error': 'Email already exists'}), 409
                
                user.email = email
            
            # Update password if provided
            if 'password' in data:
                from auth import validate_password
                password = data['password']
                valid_password, password_message = validate_password(password)
                if not valid_password:
                    return jsonify({'error': password_message}), 400
                
                user.set_password(password)
            
            user.updated_at = db.func.now()
            db.session.commit()
            
            return jsonify({'user': user.to_dict()}), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update user profile'}), 500
    
    # Database initialization
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        print('Database initialized successfully!')
    
    @app.cli.command()
    def seed_db():
        """Seed the database with sample data."""
        # Create a sample user
        if not User.query.filter_by(username='demo').first():
            demo_user = User(username='demo', email='demo@example.com')
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            db.session.commit()
            
            # Add sample expenses
            from datetime import date, timedelta
            sample_expenses = [
                {'amount': 25.50, 'description': 'Lunch at cafe', 'category': 'Food', 'date': date.today()},
                {'amount': 15.00, 'description': 'Bus fare', 'category': 'Transportation', 'date': date.today() - timedelta(days=1)},
                {'amount': 45.99, 'description': 'Grocery shopping', 'category': 'Food', 'date': date.today() - timedelta(days=2)},
                {'amount': 12.00, 'description': 'Movie ticket', 'category': 'Entertainment', 'date': date.today() - timedelta(days=3)},
                {'amount': 89.99, 'description': 'Monthly internet', 'category': 'Utilities', 'date': date.today() - timedelta(days=4)},
            ]
            
            for expense_data in sample_expenses:
                expense = Expense(
                    user_id=demo_user.id,
                    **expense_data
                )
                db.session.add(expense)
            
            db.session.commit()
            print('Database seeded with sample data!')
        else:
            print('Demo user already exists!')
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)