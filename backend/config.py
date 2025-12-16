"""
Configuration for the Flask app and database
"""

import os
from datetime import timedelta

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