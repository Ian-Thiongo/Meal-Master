"""
Authentication routes for Meal Master
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from calculations import calculate_bmr, calculate_tdee, get_activity_multiplier

# Create Blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Create a new user account"""
    data = request.json
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Validate password length
    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    try:
        # Create new user
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        # Add optional physical data if provided
        if 'weight' in data:
            user.weight_kg = float(data['weight'])
        if 'height' in data:
            user.height_cm = float(data['height'])
        if 'age' in data:
            user.age = int(data['age'])
        if 'gender' in data:
            user.gender = data['gender']
        if 'activity' in data:
            user.activity_level = data['activity']
        
        # Calculate TDEE if all data provided
        if all(key in data for key in ['weight', 'height', 'age', 'gender', 'activity']):
            bmr = calculate_bmr(
                user.weight_kg,
                user.height_cm,
                user.age,
                user.gender
            )
            multiplier = get_activity_multiplier(user.activity_level)
            if multiplier:
                user.tdee = calculate_tdee(bmr, multiplier)
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        # Create access token (convert user.id to string!)
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.json
    
    # Validate required fields
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Create access token (convert user.id to string!)
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    # Get user ID from JWT token (convert back to int!)
    user_id = int(get_jwt_identity())
    
    # Find user
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user's profile"""
    # Get user ID from JWT token (convert back to int!)
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    
    try:
        # Update fields if provided
        if 'email' in data:
            # Check if email already taken by another user
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Email already in use'}), 400
            user.email = data['email']
        
        if 'weight' in data:
            user.weight_kg = float(data['weight'])
        if 'height' in data:
            user.height_cm = float(data['height'])
        if 'age' in data:
            user.age = int(data['age'])
        if 'gender' in data:
            user.gender = data['gender']
        if 'activity' in data:
            user.activity_level = data['activity']
        
        # Recalculate TDEE if physical data changed
        if any(key in data for key in ['weight', 'height', 'age', 'gender', 'activity']):
            if all([user.weight_kg, user.height_cm, user.age, user.gender, user.activity_level]):
                bmr = calculate_bmr(
                    user.weight_kg,
                    user.height_cm,
                    user.age,
                    user.gender
                )
                multiplier = get_activity_multiplier(user.activity_level)
                if multiplier:
                    user.tdee = calculate_tdee(bmr, multiplier)
        
        # Update password if provided
        if 'password' in data:
            if len(data['password']) < 6:
                return jsonify({'error': 'Password must be at least 6 characters'}), 400
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500