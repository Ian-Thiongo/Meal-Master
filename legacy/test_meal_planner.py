from src.meal_planner import MealPlan
from src.food_api import search_food, get_food_nutrition

# Create meal plan with 2000 calorie target
print("Creating meal plan with 2000 calorie target...\n")
my_plan = MealPlan(2000)

# Search for chicken
print("Searching for chicken breast...")
chicken_results = search_food("chicken breast", max_results=1)
if chicken_results:
    print(f"Found: {chicken_results[0]['name']}\n")
    chicken_nutrition = get_food_nutrition(chicken_results[0]['fdc_id'])
    my_plan.add_food(chicken_nutrition, servings=2)

# Search for rice
print("\nSearching for rice...")
rice_results = search_food("white rice cooked", max_results=1)
if rice_results:
    print(f"Found: {rice_results[0]['name']}\n")
    rice_nutrition = get_food_nutrition(rice_results[0]['fdc_id'])
    my_plan.add_food(rice_nutrition, servings=1)

# Show summary
my_plan.show_summary()