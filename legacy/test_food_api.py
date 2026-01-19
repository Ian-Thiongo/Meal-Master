from src.food_api import search_food, get_food_nutrition

# Search for chicken
print("=== Searching for chicken breast ===\n")
results = search_food("chicken breast", max_results=3)

if results:
    print(f"Found {len(results)} results:\n")
    
    for i, food in enumerate(results, 1):
        print(f"{i}. {food['name']} - {food['brand']}")
    
    # Get nutrition for the first result
    print(f"\n=== Getting nutrition for: {results[0]['name']} ===\n")
    nutrition = get_food_nutrition(results[0]['fdc_id'])
    
    if nutrition:
        print(f"Food: {nutrition['name']}")
        print(f"Serving Size: {nutrition['serving_size']}")
        print(f"\nNutrients:")
        for nutrient, value in nutrition['nutrients'].items():
            if nutrient == 'calories':
                print(f"  Calories: {value} kcal")
            else:
                print(f"  {nutrient.capitalize()}: {value}g")