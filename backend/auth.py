"""
Authentication routes for Meal Master
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, VerificationCode
from calculations import calculate_bmr, calculate_tdee, get_activity_multiplier
from email_service import generate_verification_code, send_verification_email, get_code_expiry

# Create Blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/send-code', methods=['POST'])
def send_verification_code():
    """Send verification code to email"""
    data = request.json
    email = data.get('email')
    purpose = data.get('purpose', 'signup')  # 'signup' or 'reset'
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # For signup, check if email already exists
    if purpose == 'signup':
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered. Please login instead.'}), 400
    
    # For reset, check if email exists
    if purpose == 'reset':
        if not User.query.filter_by(email=email).first():
            return jsonify({'error': 'No account found with this email.'}), 404
    
    # Invalidate any existing codes for this email and purpose
    VerificationCode.query.filter_by(email=email, purpose=purpose, used=False).update({'used': True})
    db.session.commit()
    
    # Generate new code
    code = generate_verification_code()
    
    # Store in database
    verification = VerificationCode(
        email=email,
        code=code,
        purpose=purpose,
        expires_at=get_code_expiry()
    )
    db.session.add(verification)
    db.session.commit()
    
    # Send email
    if send_verification_email(email, code, purpose):
        return jsonify({
            'message': 'Verification code sent to your email',
            'email': email
        }), 200
    else:
        return jsonify({'error': 'Failed to send verification code'}), 500


@auth_bp.route('/verify-code', methods=['POST'])
def verify_code():
    """Verify the OTP code"""
    data = request.json
    email = data.get('email')
    code = data.get('code')
    purpose = data.get('purpose', 'signup')
    
    if not email or not code:
        return jsonify({'error': 'Email and code are required'}), 400
    
    # Find the verification code
    verification = VerificationCode.query.filter_by(
        email=email,
        code=code,
        purpose=purpose,
        used=False
    ).first()
    
    if not verification:
        return jsonify({'error': 'Invalid verification code'}), 400
    
    if not verification.is_valid():
        return jsonify({'error': 'Verification code has expired'}), 400
    
    # Mark as verified (but not used yet - will be used when signup/reset completes)
    return jsonify({
        'message': 'Code verified successfully',
        'verified': True,
        'email': email
    }), 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Create a new user account after email verification"""
    data = request.json
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'code']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Verify the code first
    verification = VerificationCode.query.filter_by(
        email=data['email'],
        code=data['code'],
        purpose='signup',
        used=False
    ).first()
    
    if not verification or not verification.is_valid():
        return jsonify({'error': 'Invalid or expired verification code'}), 400
    
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
        # Mark verification code as used
        verification.used = True
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Account created successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password after email verification"""
    data = request.json
    email = data.get('email')
    code = data.get('code')
    new_password = data.get('password')
    
    if not email or not code or not new_password:
        return jsonify({'error': 'Email, code, and new password are required'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Verify the code
    verification = VerificationCode.query.filter_by(
        email=email,
        code=code,
        purpose='reset',
        used=False
    ).first()
    
    if not verification or not verification.is_valid():
        return jsonify({'error': 'Invalid or expired verification code'}), 400
    
    # Find the user
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        # Mark code as used
        verification.used = True
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        # Create access token and log them in
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Password reset successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.json
    
    # Support login by email or username
    email_or_username = data.get('email') or data.get('username')
    password = data.get('password')
    
    if not email_or_username or not password:
        return jsonify({'error': 'Email/username and password required'}), 400
    
    # Find user by email or username
    user = User.query.filter(
        (User.email == email_or_username) | (User.username == email_or_username)
    ).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email/username or password'}), 401
    
    # Create access token
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
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user's profile (no password change here)"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    
    try:
        # Update fields if provided
        if 'email' in data:
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
        if 'is_vegetarian' in data:
            user.is_vegetarian = bool(data['is_vegetarian'])
        if 'is_vegan' in data:
            user.is_vegan = bool(data['is_vegan'])
        
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
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500