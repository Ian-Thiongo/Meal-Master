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
    
    # Calculate target calories per meal (assuming 3 meals + 2 snacks)
    daily_target = user.tdee
    meal_target = daily_target / 4  # Approximate per-meal target
    
    # Food categories for variety
    categories = [
        'chicken breast',
        'salmon',
        'eggs',
        'brown rice',
        'oatmeal',
        'banana',
        'broccoli',
        'almonds',
        'greek yogurt',
        'sweet potato',
        'spinach',
        'avocado',
        'quinoa',
        'turkey',
        'black beans',
        'cottage cheese',
        'apple',
        'whole wheat bread'
    ]
    
    # Randomly select 5 different categories
    selected_categories = random.sample(categories, min(5, len(categories)))
    
    recommendations = []
    
    for category in selected_categories:
        results = search_usda_foods(category, page_size=5, data_type="Foundation,Survey (FNDDS)")
        
        if results and results.get('foods'):
            # Pick a random food from results for variety
            food = random.choice(results['foods'])
            formatted = format_food_result(food)
            
            if formatted['calories'] > 0:
                # Calculate suggested serving to meet ~25% of daily target
                if formatted['calories'] > 0:
                    suggested_servings = round(meal_target / formatted['calories'], 1)
                    formatted['suggested_servings'] = min(suggested_servings, 3)  # Cap at 3 servings
                    formatted['suggested_calories'] = round(formatted['calories'] * formatted['suggested_servings'])
                
                recommendations.append(formatted)
    
    return jsonify({
        'daily_target': round(daily_target),
        'recommendations': recommendations
    })