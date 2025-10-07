from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from models import db, Expense, User
from auth import auth_required
from sqlalchemy import and_, or_

expenses_bp = Blueprint('expenses', __name__, url_prefix='/api/expenses')

@expenses_bp.route('', methods=['GET'])
@jwt_required()
def get_expenses():
    """Get user's expenses with optional filtering and pagination."""
    try:
        current_user_id_str = get_jwt_identity()
        print(f"DEBUG: Expenses request - current_user_id from JWT: {current_user_id_str}")
        
        if current_user_id_str is None:
            print("DEBUG: JWT identity is None - token might be invalid")
            return jsonify({'error': 'Invalid token - no user identity'}), 401
        
        # Convert string ID back to integer for database queries
        current_user_id = int(current_user_id_str)
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', current_app.config['EXPENSES_PER_PAGE'], type=int)
        category = request.args.get('category')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Build query
        query = Expense.query.filter_by(user_id=current_user_id)
        
        # Apply filters
        if category:
            query = query.filter(Expense.category == category)
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                query = query.filter(Expense.date >= date_from_obj)
            except ValueError:
                return jsonify({'error': 'Invalid date_from format. Use YYYY-MM-DD'}), 400
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                query = query.filter(Expense.date <= date_to_obj)
            except ValueError:
                return jsonify({'error': 'Invalid date_to format. Use YYYY-MM-DD'}), 400
        
        # Order by date descending
        query = query.order_by(Expense.date.desc(), Expense.created_at.desc())
        
        # Paginate
        pagination = query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        expenses = [expense.to_dict() for expense in pagination.items]
        
        return jsonify({
            'expenses': expenses,
            'total': pagination.total,
            'page_info': {
                'page': page,
                'pages': pagination.pages,
                'per_page': limit,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve expenses'}), 500

@expenses_bp.route('', methods=['POST'])
@jwt_required()
def create_expense():
    """Create a new expense."""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        amount = data.get('amount')
        description = data.get('description', '').strip()
        category = data.get('category', '').strip()
        expense_date = data.get('date')
        
        if not all([amount, description, category, expense_date]):
            return jsonify({'error': 'Amount, description, category, and date are required'}), 400
        
        # Validate amount
        try:
            amount = float(amount)
            if amount <= 0:
                return jsonify({'error': 'Amount must be greater than 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount format'}), 400
        
        # Validate category
        if category not in current_app.config['EXPENSE_CATEGORIES']:
            return jsonify({'error': f'Invalid category. Must be one of: {", ".join(current_app.config["EXPENSE_CATEGORIES"])}'}), 400
        
        # Validate date
        try:
            expense_date_obj = datetime.strptime(expense_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Validate description length
        if len(description) > 255:
            return jsonify({'error': 'Description must be less than 255 characters'}), 400
        
        # Create expense
        expense = Expense(
            user_id=current_user_id,
            amount=amount,
            description=description,
            category=category,
            date=expense_date_obj
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({'expense': expense.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create expense'}), 500

@expenses_bp.route('/<int:expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id):
    """Get a specific expense."""
    try:
        current_user_id = int(get_jwt_identity())
        
        expense = Expense.query.filter_by(id=expense_id, user_id=current_user_id).first()
        
        if not expense:
            return jsonify({'error': 'Expense not found'}), 404
        
        return jsonify({'expense': expense.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve expense'}), 500

@expenses_bp.route('/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    """Update an existing expense."""
    try:
        current_user_id = int(get_jwt_identity())
        
        expense = Expense.query.filter_by(id=expense_id, user_id=current_user_id).first()
        
        if not expense:
            return jsonify({'error': 'Expense not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    return jsonify({'error': 'Amount must be greater than 0'}), 400
                expense.amount = amount
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid amount format'}), 400
        
        if 'description' in data:
            description = data['description'].strip()
            if len(description) > 255:
                return jsonify({'error': 'Description must be less than 255 characters'}), 400
            expense.description = description
        
        if 'category' in data:
            category = data['category'].strip()
            if category not in current_app.config['EXPENSE_CATEGORIES']:
                return jsonify({'error': f'Invalid category. Must be one of: {", ".join(current_app.config["EXPENSE_CATEGORIES"])}'}), 400
            expense.category = category
        
        if 'date' in data:
            try:
                expense_date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
                expense.date = expense_date_obj
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        expense.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'expense': expense.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update expense'}), 500

@expenses_bp.route('/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    """Delete an expense."""
    try:
        current_user_id = int(get_jwt_identity())
        
        expense = Expense.query.filter_by(id=expense_id, user_id=current_user_id).first()
        
        if not expense:
            return jsonify({'error': 'Expense not found'}), 404
        
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({'message': 'Expense deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete expense'}), 500

@expenses_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get available expense categories."""
    try:
        return jsonify({'categories': current_app.config['EXPENSE_CATEGORIES']}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve categories'}), 500

@expenses_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_expense_summary():
    """Get expense summary for the current user."""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Get total expenses
        total_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=current_user_id).scalar() or 0
        
        # Get expenses by category
        category_summary = db.session.query(
            Expense.category,
            db.func.sum(Expense.amount).label('total'),
            db.func.count(Expense.id).label('count')
        ).filter_by(user_id=current_user_id).group_by(Expense.category).all()
        
        # Get recent expenses count
        recent_count = Expense.query.filter_by(user_id=current_user_id).count()
        
        return jsonify({
            'total_amount': float(total_expenses),
            'total_count': recent_count,
            'categories': [
                {
                    'category': cat.category,
                    'total': float(cat.total),
                    'count': cat.count
                }
                for cat in category_summary
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve expense summary'}), 500