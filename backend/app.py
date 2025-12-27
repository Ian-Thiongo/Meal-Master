"""
Main Flask application for Meal Master
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db, bcrypt
from auth import auth_bp
from food_api import food_bp
from meals import meals_bp
from calculations import calculate_bmr, calculate_tdee, get_activity_multiplier


def create_app():
    """Application factory"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    CORS(app)  # Allow requests from React frontend

    # Create database tables
    with app.app_context():
        db.create_all()
        print("✓ Database tables created!")
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(food_bp, url_prefix='/api/food')
    app.register_blueprint(meals_bp, url_prefix='/api/meals')
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'ok', 'message': 'Meal Master API is running!'})

    # TDEE calculation endpoint
    @app.route('/api/calculate_tdee', methods=['POST'])
    def calculate_tdee_route():
        data = request.json

        # Validate input
        required_fields = ['weight', 'height', 'age', 'gender', 'activity']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            # Calculate BMR
            bmr = calculate_bmr(
                float(data['weight']),
                float(data['height']),
                int(data['age']),
                data['gender']
            )

            # Get activity multiplier
            multiplier = get_activity_multiplier(data['activity'])
            if not multiplier:
                return jsonify({'error': 'Invalid activity level'}), 400

            # Calculate TDEE
            tdee = calculate_tdee(bmr, multiplier)

            return jsonify({
                'bmr': bmr,
                'tdee': tdee,
                'activity_multiplier': multiplier
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)