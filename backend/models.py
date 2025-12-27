"""
Database models for Meal Master
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    """User model for storing user data"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # User physical data
    weight_kg = db.Column(db.Float, nullable=True)
    height_cm = db.Column(db.Float, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    activity_level = db.Column(db.String(20), nullable=True)
    tdee = db.Column(db.Float, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    meal_plans = db.relationship('MealPlan', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if password matches the hash"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user to dictionary (for JSON responses)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'weight_kg': self.weight_kg,
            'height_cm': self.height_cm,
            'age': self.age,
            'gender': self.gender,
            'activity_level': self.activity_level,
            'tdee': self.tdee,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class MealPlan(db.Model):
    """Meal plan model for storing daily meal plans"""
    __tablename__ = 'meal_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    tdee_target = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    meals = db.relationship('Meal', backref='meal_plan', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convert meal plan to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'tdee_target': self.tdee_target,
            'meals': [meal.to_dict() for meal in self.meals],
            'total_calories': sum(meal.calories for meal in self.meals)
        }


class Meal(db.Model):
    """Meal model for storing individual foods in a meal plan"""
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plans.id'), nullable=False)

    # Food data
    food_name = db.Column(db.String(255), nullable=False)
    fdc_id = db.Column(db.Integer, nullable=True)
    servings = db.Column(db.Float, nullable=False)

    # Nutritional data
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=True)
    carbs = db.Column(db.Float, nullable=True)
    fats = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert meal to dictionary (for JSON responses)"""
        return {
            'id': self.id,
            'meal_plan_id': self.meal_plan_id,
            'food_name': self.food_name,
            'fdc_id': self.fdc_id,
            'servings': self.servings,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fats': self.fats,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }