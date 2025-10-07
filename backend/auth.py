from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import User

def auth_required(f):
    """Decorator to require authentication for routes."""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 401
        
        return f(current_user=current_user, *args, **kwargs)
    
    return decorated_function

def get_current_user():
    """Get the current authenticated user."""
    current_user_id = get_jwt_identity()
    if current_user_id:
        return User.query.get(current_user_id)
    return None

def validate_user_ownership(user_id, resource_user_id):
    """Validate that the current user owns the resource."""
    return user_id == resource_user_id

# JWT token blacklist (in production, use Redis or database)
blacklisted_tokens = set()

def is_token_blacklisted(jwt_payload):
    """Check if a JWT token is blacklisted."""
    jti = jwt_payload['jti']
    return jti in blacklisted_tokens

def blacklist_token(jti):
    """Add a token to the blacklist."""
    blacklisted_tokens.add(jti)

def validate_password(password):
    """Validate password strength."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid"

def validate_email(email):
    """Basic email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, "Email is valid"
    return False, "Invalid email format"

def validate_username(username):
    """Validate username."""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if len(username) > 80:
        return False, "Username must be less than 80 characters"
    return True, "Username is valid"