from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User
from auth import validate_password, validate_email, validate_username, blacklist_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validate required fields
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        # Validate username
        valid_username, username_message = validate_username(username)
        if not valid_username:
            return jsonify({'error': username_message}), 400
        
        # Validate email
        valid_email, email_message = validate_email(email)
        if not valid_email:
            return jsonify({'error': email_message}), 400
        
        # Validate password
        valid_password, password_message = validate_password(password)
        if not valid_password:
            return jsonify({'error': password_message}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Debug: Log user info
        print(f"DEBUG: Login successful for user ID: {user.id}, username: {user.username}")
        print(f"DEBUG: JWT_SECRET_KEY during token creation: {current_app.config.get('JWT_SECRET_KEY', 'NOT_SET')}")
        
        try:
            # Create JWT tokens
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            
            print(f"DEBUG: Generated token for user_id {user.id}: {access_token[:50]}...")
            
            user_dict = user.to_dict()
            print(f"DEBUG: User dict: {user_dict}")
            
            return jsonify({
                'token': access_token,
                'refresh_token': refresh_token,
                'user_info': user_dict
            }), 200
        except Exception as e:
            print(f"DEBUG: Exception during token creation or response: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': 'Login failed'}), 500
        
    except Exception as e:
        print(f"ERROR: Login exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user and blacklist token."""
    try:
        jti = get_jwt()['jti']
        blacklist_token(jti)
        
        return jsonify({'message': 'Successfully logged out'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Logout failed'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information."""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user_info': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user information'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh JWT access token."""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        new_access_token = create_access_token(identity=str(current_user_id))
        
        return jsonify({'token': new_access_token}), 200
        
    except Exception as e:
        return jsonify({'error': 'Token refresh failed'}), 500