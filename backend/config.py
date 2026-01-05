"""
Configuration for the Flask app and database
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Get the base directory (where the backend folder is)
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration"""

    # Secret key for JWT tokens (change this to a random string in production!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-this-in-production'

    # SQLite database path
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'meal_master.db')

    # Disable modification tracking (saves resources)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-this'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Tokens expire after 24 hours

    # USDA API Key
    USDA_API_KEY = os.environ.get('USDA_API_KEY')

    # Google OAuth Settings
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    
    # Frontend URL for redirects
    FRONTEND_URL = os.environ.get('FRONTEND_URL') or 'http://localhost:5173'
    
    # Email Settings (for verification codes)
    EMAIL_HOST = os.environ.get('EMAIL_HOST') or 'smtp.gmail.com'
    EMAIL_PORT = os.environ.get('EMAIL_PORT') or 587
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    EMAIL_FROM = os.environ.get('EMAIL_FROM')