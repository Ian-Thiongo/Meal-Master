import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv('USDA_API_KEY')

if not api_key:
    print("ERROR: No API key found in .env file!")
    exit(1)

print(f"API Key loaded: {api_key[:10]}...{api_key[-4:]}")  # Show partial key for security
print("\nTesting USDA Food API...")

# Test the USDA FoodData Central API
url = "https://api.nal.usda.gov/fdc/v1/foods/search"
params = {
    "query": "fermented milk",
    "api_key": api_key  # Now using your real API key!
}

print(f"Searching for: {params['query']}\n")

response = requests.get(url, params=params)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    foods = data.get('foods', [])
    print(f"✓ Found {len(foods)} foods\n")
    
    # Print first 3 results
    for i, food in enumerate(foods[:3], 1):
        print(f"{i}. {food.get('description')}")
        print(f"   FDC ID: {food.get('fdcId')}")
        
        # Get calories if available
        nutrients = food.get('foodNutrients', [])
        for nutrient in nutrients:
            if nutrient.get('nutrientName') == 'Energy':
                print(f"   Calories: {nutrient.get('value')} kcal per 100g")
                break
        print()
else:
    print(f"✗ Error: {response.status_code}")
    print(response.text)