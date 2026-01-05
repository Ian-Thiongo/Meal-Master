"""
Food search and recommendation routes using USDA API
"""

import requests
import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config
from models import db, User

food_bp = Blueprint('food', __name__)

USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1"


def search_usda_foods(query, page_size=25, data_type=None):
    """Search USDA database for foods"""
    url = f"{USDA_BASE_URL}/foods/search"
    
    params = {
        "api_key": Config.USDA_API_KEY,
        "query": query,
        "pageSize": page_size,
    }
    
    # Filter by data type (Foundation, Survey, Branded, etc.)
    if data_type:
        params["dataType"] = data_type
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"USDA API error: {e}")
        return None


def get_food_details(fdc_id):
    """Get detailed nutrition info for a specific food"""
    url = f"{USDA_BASE_URL}/food/{fdc_id}"
    
    params = {
        "api_key": Config.USDA_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"USDA API error: {e}")
        return None


def extract_nutrients(food_data):
    """Extract key nutrients from USDA food data"""
    nutrients = {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0,
        'fiber': 0
    }
    
    # Nutrient IDs in USDA database
    nutrient_ids = {
        1008: 'calories',  # Energy (kcal)
        1003: 'protein',   # Protein
        1005: 'carbs',     # Carbohydrates
        1004: 'fat',       # Total fat
        1079: 'fiber'      # Fiber
    }
    
    food_nutrients = food_data.get('foodNutrients', [])
    
    for nutrient in food_nutrients:
        # Handle different response formats
        nutrient_id = nutrient.get('nutrientId') or nutrient.get('nutrient', {}).get('id')
        
        if nutrient_id in nutrient_ids:
            value = nutrient.get('value') or nutrient.get('amount', 0)
            nutrients[nutrient_ids[nutrient_id]] = round(value, 1)
    
    return nutrients


def format_food_result(food):
    """Format a food item for the frontend"""
    nutrients = extract_nutrients(food)
    
    return {
        'fdc_id': food.get('fdcId'),
        'name': food.get('description', 'Unknown'),
        'brand': food.get('brandOwner', 'Generic'),
        'category': food.get('foodCategory', 'Uncategorized'),
        'serving_size': food.get('servingSize', 100),
        'serving_unit': food.get('servingSizeUnit', 'g'),
        'calories': nutrients['calories'],
        'protein': nutrients['protein'],
        'carbs': nutrients['carbs'],
        'fat': nutrients['fat'],
        'fiber': nutrients['fiber']
    }


@food_bp.route('/search', methods=['GET'])
@jwt_required()
def search_foods():
    """Search for foods by name"""
    query = request.args.get('q', '')
    page_size = request.args.get('limit', 20, type=int)
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    if len(query) < 2:
        return jsonify({'error': 'Query must be at least 2 characters'}), 400
    
    # Search USDA database
    results = search_usda_foods(query, page_size=page_size)
    
    if not results:
        return jsonify({'error': 'Failed to fetch from USDA API'}), 500
    
    # Format results
    foods = []
    for food in results.get('foods', []):
        formatted = format_food_result(food)
        if formatted['calories'] > 0:  # Only include foods with calorie data
            foods.append(formatted)
    
    return jsonify({
        'query': query,
        'total_results': results.get('totalHits', 0),
        'foods': foods
    })


@food_bp.route('/details/<int:fdc_id>', methods=['GET'])
@jwt_required()
def get_food(fdc_id):
    """Get detailed info for a specific food"""
    food_data = get_food_details(fdc_id)
    
    if not food_data:
        return jsonify({'error': 'Food not found'}), 404
    
    return jsonify(format_food_result(food_data))


# Food lists for recommendations
VEGETARIAN_BREAKFAST = ['oatmeal', 'eggs', 'greek yogurt', 'banana', 'avocado toast', 'smoothie bowl', 'pancakes', 'fruit salad']
VEGETARIAN_LUNCH = ['quinoa salad', 'lentil soup', 'chickpea curry', 'grilled cheese', 'veggie wrap', 'falafel', 'caprese salad', 'hummus bowl']
VEGETARIAN_DINNER = ['tofu stir fry', 'vegetable pasta', 'black bean tacos', 'paneer tikka', 'mushroom risotto', 'eggplant parmesan', 'stuffed peppers', 'vegetable curry']

VEGAN_BREAKFAST = ['oatmeal', 'banana', 'avocado toast', 'smoothie bowl', 'fruit salad', 'chia pudding', 'granola', 'toast with peanut butter']
VEGAN_LUNCH = ['quinoa salad', 'lentil soup', 'chickpea curry', 'veggie wrap', 'falafel', 'hummus bowl', 'black bean soup', 'vegetable stir fry']
VEGAN_DINNER = ['tofu stir fry', 'vegetable pasta', 'black bean tacos', 'mushroom risotto', 'stuffed peppers', 'vegetable curry', 'lentil dal', 'buddha bowl']

NON_VEG_BREAKFAST = ['eggs', 'turkey bacon', 'oatmeal', 'greek yogurt', 'breakfast burrito', 'smoothie', 'avocado toast']
NON_VEG_LUNCH = ['chicken breast', 'salmon', 'tuna salad', 'turkey sandwich', 'beef stir fry', 'grilled chicken salad', 'shrimp bowl']
NON_VEG_DINNER = ['grilled salmon', 'chicken breast', 'beef steak', 'pork tenderloin', 'shrimp pasta', 'turkey meatballs', 'baked fish']


def get_meal_recommendations(meal_type, calories_target, is_vegetarian=False, is_vegan=False):
    """Get food recommendations for a specific meal type"""
    # Vegan takes priority (stricter diet)
    if is_vegan:
        if meal_type == 'breakfast':
            food_list = VEGAN_BREAKFAST
        elif meal_type == 'lunch':
            food_list = VEGAN_LUNCH
        else:
            food_list = VEGAN_DINNER
    elif is_vegetarian:
        if meal_type == 'breakfast':
            food_list = VEGETARIAN_BREAKFAST
        elif meal_type == 'lunch':
            food_list = VEGETARIAN_LUNCH
        else:
            food_list = VEGETARIAN_DINNER
    else:
        if meal_type == 'breakfast':
            food_list = NON_VEG_BREAKFAST
        elif meal_type == 'lunch':
            food_list = NON_VEG_LUNCH
        else:
            food_list = NON_VEG_DINNER
    
    # Select 2-3 random foods for variety
    selected = random.sample(food_list, min(3, len(food_list)))
    recommendations = []
    
    for food_name in selected:
        results = search_usda_foods(food_name, page_size=3, data_type="Foundation,Survey (FNDDS)")
        
        if results and results.get('foods'):
            food = random.choice(results['foods'])
            formatted = format_food_result(food)
            
            if formatted['calories'] > 0:
                # Calculate suggested servings to hit calorie target
                suggested_servings = round(calories_target / formatted['calories'], 1)
                formatted['suggested_servings'] = max(0.5, min(suggested_servings, 3))
                formatted['suggested_calories'] = round(formatted['calories'] * formatted['suggested_servings'])
                formatted['meal_type'] = meal_type
                recommendations.append(formatted)
    
    return recommendations


@food_bp.route('/meal-plan-suggestions', methods=['GET'])
@jwt_required()
def get_meal_plan_suggestions():
    """
    Get TDEE-balanced meal suggestions for breakfast, lunch, and dinner.
    Respects vegetarian preference.
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not user.tdee:
        return jsonify({'error': 'Please complete your profile to get meal suggestions'}), 400
    
    daily_target = user.tdee
    is_vegetarian = user.is_vegetarian or False
    is_vegan = user.is_vegan or False
    
    # TDEE split: Breakfast 25%, Lunch 35%, Dinner 30%, Snacks 10%
    breakfast_target = round(daily_target * 0.25)
    lunch_target = round(daily_target * 0.35)
    dinner_target = round(daily_target * 0.30)
    snack_target = round(daily_target * 0.10)
    
    # Get recommendations for each meal
    breakfast_recs = get_meal_recommendations('breakfast', breakfast_target, is_vegetarian, is_vegan)
    lunch_recs = get_meal_recommendations('lunch', lunch_target, is_vegetarian, is_vegan)
    dinner_recs = get_meal_recommendations('dinner', dinner_target, is_vegetarian, is_vegan)
    
    return jsonify({
        'daily_target': round(daily_target),
        'is_vegetarian': is_vegetarian,
        'is_vegan': is_vegan,
        'meal_targets': {
            'breakfast': breakfast_target,
            'lunch': lunch_target,
            'dinner': dinner_target,
            'snacks': snack_target
        },
        'suggestions': {
            'breakfast': breakfast_recs,
            'lunch': lunch_recs,
            'dinner': dinner_recs
        }
    })


@food_bp.route('/daily-status', methods=['GET'])
@jwt_required()
def get_daily_status():
    """
    Get daily nutrition status with time-aware prompts.
    Returns consumed calories, remaining calories, and meal prompts.
    """
    from datetime import date
    from models import MealPlan
    
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get client's local hour from query param (frontend sends this)
    client_hour = request.args.get('hour', type=int)
    if client_hour is None:
        # Default to server time if not provided
        from datetime import datetime
        client_hour = datetime.now().hour
    
    # Determine time of day and appropriate prompt
    if 5 <= client_hour < 11:
        time_of_day = 'morning'
        greeting = "Good morning! ☀️"
        prompt = "Ready to plan your breakfast?"
        meals_to_log = []
    elif 11 <= client_hour < 14:
        time_of_day = 'noon'
        greeting = "Good afternoon! 🌤️"
        prompt = "Have you logged your breakfast yet?"
        meals_to_log = ['breakfast']
    elif 14 <= client_hour < 18:
        time_of_day = 'afternoon'
        greeting = "Good afternoon! 🌅"
        prompt = "How was lunch? Don't forget to log it!"
        meals_to_log = ['breakfast', 'lunch']
    elif 18 <= client_hour < 21:
        time_of_day = 'evening'
        greeting = "Good evening! 🌙"
        prompt = "Time to plan dinner! Log any meals you haven't yet."
        meals_to_log = ['breakfast', 'lunch']
    else:
        time_of_day = 'night'
        greeting = "Good night! 🌜"
        prompt = "Log any remaining meals before the day ends."
        meals_to_log = ['breakfast', 'lunch', 'dinner']
    
    # Get today's meal plan
    today = date.today()
    meal_plan = MealPlan.query.filter_by(user_id=user_id, date=today).first()
    
    consumed_calories = 0
    meals_logged = []
    
    if meal_plan:
        consumed_calories = sum(meal.calories for meal in meal_plan.meals)
        meals_logged = [meal.to_dict() for meal in meal_plan.meals]
    
    # Calculate remaining
    daily_target = user.tdee or 2000
    remaining_calories = max(0, daily_target - consumed_calories)
    progress_percent = min(100, round((consumed_calories / daily_target) * 100))
    
    return jsonify({
        'time_of_day': time_of_day,
        'greeting': greeting,
        'prompt': prompt,
        'meals_to_log': meals_to_log,
        'daily_target': round(daily_target),
        'consumed_calories': round(consumed_calories),
        'remaining_calories': round(remaining_calories),
        'progress_percent': progress_percent,
        'meals_logged': meals_logged
    })


@food_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get personalized food recommendations based on user's TDEE"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not user.tdee:
        return jsonify({'error': 'Please complete your profile to get recommendations'}), 400
    
    daily_target = user.tdee
    meal_target = daily_target / 4
    is_vegetarian = user.is_vegetarian or False
    
    # Choose foods based on dietary preference
    if is_vegetarian:
        categories = VEGETARIAN_BREAKFAST + VEGETARIAN_LUNCH + VEGETARIAN_DINNER
    else:
        categories = NON_VEG_BREAKFAST + NON_VEG_LUNCH + NON_VEG_DINNER
    
    selected_categories = random.sample(categories, min(5, len(categories)))
    recommendations = []
    
    for category in selected_categories:
        results = search_usda_foods(category, page_size=5, data_type="Foundation,Survey (FNDDS)")
        
        if results and results.get('foods'):
            food = random.choice(results['foods'])
            formatted = format_food_result(food)
            
            if formatted['calories'] > 0:
                suggested_servings = round(meal_target / formatted['calories'], 1)
                formatted['suggested_servings'] = min(suggested_servings, 3)
                formatted['suggested_calories'] = round(formatted['calories'] * formatted['suggested_servings'])
                recommendations.append(formatted)
    
    return jsonify({
        'daily_target': round(daily_target),
        'is_vegetarian': is_vegetarian,
        'recommendations': recommendations
    })