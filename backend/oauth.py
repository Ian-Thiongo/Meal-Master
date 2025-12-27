"""
Google OAuth routes for Meal Master
"""

import json
import requests
from flask import Blueprint, redirect, request, jsonify, url_for
from flask_jwt_extended import create_access_token
from authlib.integrations.flask_client import OAuth
from config import Config
from models import db, User

oauth_bp = Blueprint('oauth', __name__)

# Initialize OAuth
oauth = OAuth()

def init_oauth(app):
    """Initialize OAuth with the Flask app"""
    oauth.init_app(app)
    
    oauth.register(
        name='google',
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        server_metadata_url=Config.GOOGLE_DISCOVERY_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


@oauth_bp.route('/google/login')
def google_login():
    """Redirect to Google OAuth"""
    redirect_uri = url_for('oauth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@oauth_bp.route('/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        # Get the token from Google
        token = oauth.google.authorize_access_token()
        
        # Get user info from Google
        user_info = token.get('userinfo')
        
        if not user_info:
            # Fetch user info from Google's userinfo endpoint
            resp = oauth.google.get('https://openidconnect.googleapis.com/v1/userinfo')
            user_info = resp.json()
        
        google_id = user_info.get('sub')
        email = user_info.get('email')
        name = user_info.get('name', email.split('@')[0])
        
        if not email:
            return redirect(f"{Config.FRONTEND_URL}/login?error=Google login failed - no email provided")
        
        # Check if user exists by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create new user
            # Generate username from email or name
            base_username = name.replace(' ', '_').lower()
            username = base_username
            counter = 1
            
            # Ensure unique username
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User(
                username=username,
                email=email
            )
            # Set a random password (user won't use it, they'll login with Google)
            import secrets
            user.set_password(secrets.token_urlsafe(32))
            
            db.session.add(user)
            db.session.commit()
        
        # Create JWT token
        access_token = create_access_token(identity=str(user.id))
        
        # Redirect to frontend with token
        return redirect(f"{Config.FRONTEND_URL}/oauth/callback?token={access_token}")
        
    except Exception as e:
        print(f"OAuth error: {e}")
        return redirect(f"{Config.FRONTEND_URL}/login?error=Google login failed")


@oauth_bp.route('/google/token', methods=['POST'])
def google_token_login():
    """
    Alternative: Login with Google ID token from frontend
    This is for the popup/redirect flow handled by frontend
    """
    data = request.json
    credential = data.get('credential')
    
    if not credential:
        return jsonify({'error': 'No credential provided'}), 400
    
    try:
        # Verify the token with Google
        google_response = requests.get(
            f'https://oauth2.googleapis.com/tokeninfo?id_token={credential}'
        )
        
        if google_response.status_code != 200:
            return jsonify({'error': 'Invalid Google token'}), 401
        
        user_info = google_response.json()
        
        # Verify the token is for our app
        if user_info.get('aud') != Config.GOOGLE_CLIENT_ID:
            return jsonify({'error': 'Token not intended for this app'}), 401
        
        email = user_info.get('email')
        name = user_info.get('name', email.split('@')[0])
        
        if not email:
            return jsonify({'error': 'No email in Google account'}), 400
        
        # Find or create user
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create new user
            base_username = name.replace(' ', '_').lower()
            username = base_username
            counter = 1
            
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User(
                username=username,
                email=email
            )
            import secrets
            user.set_password(secrets.token_urlsafe(32))
            
            db.session.add(user)
            db.session.commit()
        
        # Create JWT token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Google token login error: {e}")
        return jsonify({'error': 'Google login failed'}), 500


