"""
Meal Plan routes for Meal Master
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from models import db, User, MealPlan, Meal

meals_bp = Blueprint('meals', __name__)


@meals_bp.route('/plans', methods=['GET'])
@jwt_required()
def get_meal_plans():
    """Get all meal plans for the current user"""
    user_id = int(get_jwt_identity())
    
    # Get optional date filter
    date_str = request.args.get('date')
    
    query = MealPlan.query.filter_by(user_id=user_id)
    
    if date_str:
        try:
            filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter_by(date=filter_date)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    meal_plans = query.order_by(MealPlan.date.desc()).all()
    
    return jsonify({
        'meal_plans': [plan.to_dict() for plan in meal_plans]
    })


@meals_bp.route('/plans/today', methods=['GET'])
@jwt_required()
def get_todays_plan():
    """Get or create today's meal plan"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    today = date.today()
    
    # Find existing plan for today
    meal_plan = MealPlan.query.filter_by(user_id=user_id, date=today).first()
    
    # Create new plan if none exists
    if not meal_plan:
        tdee_target = user.tdee or 2000  # Default to 2000 if no TDEE set
        meal_plan = MealPlan(
            user_id=user_id,
            date=today,
            tdee_target=tdee_target
        )
        db.session.add(meal_plan)
        db.session.commit()
    
    return jsonify(meal_plan.to_dict())


@meals_bp.route('/plans/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_meal_plan(plan_id):
    """Get a specific meal plan"""
    user_id = int(get_jwt_identity())
    
    meal_plan = MealPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    
    if not meal_plan:
        return jsonify({'error': 'Meal plan not found'}), 404
    
    return jsonify(meal_plan.to_dict())


@meals_bp.route('/plans/<int:plan_id>/meals', methods=['POST'])
@jwt_required()
def add_meal_to_plan(plan_id):
    """Add a meal/food to a meal plan"""
    user_id = int(get_jwt_identity())
    
    # Verify ownership
    meal_plan = MealPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    
    if not meal_plan:
        return jsonify({'error': 'Meal plan not found'}), 404
    
    data = request.json
    
    # Validate required fields
    required_fields = ['food_name', 'calories', 'servings']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields: food_name, calories, servings'}), 400
    
    try:
        meal = Meal(
            meal_plan_id=plan_id,
            food_name=data['food_name'],
            fdc_id=data.get('fdc_id'),
            servings=float(data['servings']),
            calories=float(data['calories']) * float(data['servings']),
            protein=float(data.get('protein', 0)) * float(data['servings']),
            carbs=float(data.get('carbs', 0)) * float(data['servings']),
            fats=float(data.get('fat', 0)) * float(data['servings'])
        )
        
        db.session.add(meal)
        db.session.commit()
        
        return jsonify({
            'message': 'Meal added successfully',
            'meal': meal.to_dict(),
            'meal_plan': meal_plan.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@meals_bp.route('/plans/<int:plan_id>/meals/<int:meal_id>', methods=['DELETE'])
@jwt_required()
def remove_meal_from_plan(plan_id, meal_id):
    """Remove a meal from a meal plan"""
    user_id = int(get_jwt_identity())
    
    # Verify ownership
    meal_plan = MealPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    
    if not meal_plan:
        return jsonify({'error': 'Meal plan not found'}), 404
    
    meal = Meal.query.filter_by(id=meal_id, meal_plan_id=plan_id).first()
    
    if not meal:
        return jsonify({'error': 'Meal not found'}), 404
    
    try:
        db.session.delete(meal)
        db.session.commit()
        
        return jsonify({
            'message': 'Meal removed successfully',
            'meal_plan': meal_plan.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@meals_bp.route('/plans/<int:plan_id>', methods=['DELETE'])
@jwt_required()
def delete_meal_plan(plan_id):
    """Delete a meal plan"""
    user_id = int(get_jwt_identity())
    
    meal_plan = MealPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    
    if not meal_plan:
        return jsonify({'error': 'Meal plan not found'}), 404
    
    try:
        db.session.delete(meal_plan)
        db.session.commit()
        
        return jsonify({'message': 'Meal plan deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

