"""
Food API Module
Handles all interactions with USDA FoodData Central API
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv('USDA_API_KEY')
BASE_URL = "https://api.nal.usda.gov/fdc/v1"


def search_food(query, max_results=10):
    """
    Search for foods by name
    
    Args:
        query: The food name to search for (e.g., "apple")
        max_results: How many results to return (default is 10)
    
    Returns:
        A list of food dictionaries, or None if the request fails
    """
    # Check if we have an API key
    if not API_KEY:
        print("ERROR: No API key found!")
        return None
    
    # Build the URL
    url = f"{BASE_URL}/foods/search"
    
    # Prepare parameters
    params = {
        "query": query,
        "pageSize": max_results,  # Limit results
        "api_key": API_KEY
    }
    
    # Make the request
    response = requests.get(url, params=params)
    
    # Check if successful
    if response.status_code == 200:
        data = response.json()
        foods = data.get('foods', [])
        
        # Creating a simplified list
        results = []
        for food in foods:
            results.append({
                'fdc_id': food.get('fdcId'),
                'name': food.get('description'),
                'brand': food.get('brandName', 'Generic')
            })
        
        return results
    else:
        print(f"API Error: {response.status_code}")
        return None


def get_food_nutrition(fdc_id):
    """
    Get detailed nutrition info for a specific food
    
    Args:
        fdc_id (int): The FDC ID of the food
    
    Returns:
        dict: Nutrition information (calories, protein, carbs, fats)
        None: If the request fails
    """
    if not API_KEY:
        print("ERROR: No API key found")
        return None
    
    url = f"{BASE_URL}/food/{fdc_id}"
    params = {"api_key": API_KEY}
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract key nutrients
            nutrients = {}
            nutrient_list = data.get('foodNutrients', [])
            
            # Mapping of nutrient names to look for
            nutrient_map = {
                'Energy': 'calories',
                'Protein': 'protein',
                'Carbohydrate, by difference': 'carbs',
                'Total lipid (fat)': 'fats'
            }
            
            for nutrient in nutrient_list:
                nutrient_name = nutrient.get('nutrient', {}).get('name')
                
                if nutrient_name in nutrient_map:
                    key = nutrient_map[nutrient_name]
                    nutrients[key] = round(nutrient.get('amount', 0), 1)
            
            return {
                'name': data.get('description'),
                'fdc_id': fdc_id,
                'serving_size': '100g',  # USDA data is per 100g
                'nutrients': nutrients
            }
        else:
            print(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Request failed: {e}")
        return None


# Test the functions if this file is run directly
if __name__ == "__main__":
    print("Testing food_api.py...\n")
    
    # Test search
    print("Searching for 'chicken breast'...")
    results = search_food("chicken breast", max_results=3)
    
    if results:
        print(f"Found {len(results)} results:\n")
        for i, food in enumerate(results, 1):
            print(f"{i}. {food['name']}")
            print(f"   Brand: {food['brand']}")
            print(f"   FDC ID: {food['fdc_id']}\n")
        
        # Test nutrition details for first result
        if results:
            print(f"\nGetting nutrition for: {results[0]['name']}")
            nutrition = get_food_nutrition(results[0]['fdc_id'])
            
            if nutrition:
                print(f"\nNutrition per {nutrition['serving_size']}:")
                for nutrient, value in nutrition['nutrients'].items():
                    print(f"  {nutrient.capitalize()}: {value}g" if nutrient != 'calories' else f"  Calories: {value} kcal")