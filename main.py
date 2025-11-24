"""
Meal Master - Complete Meal Planning Application
"""

from src.user_input import get_user_input
from src.calculations import calculate_bmr, calculate_tdee, get_activity_multiplier
from src.food_api import search_food, get_food_nutrition
from src.meal_planner import MealPlan


def print_header():
    """Print the application header"""
    print("\n" + "="*50)
    print("     MEAL MASTER - Meal Planner")
    print("="*50)


def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("           MAIN MENU")
    print("="*50)
    print("1. Search and add food")
    print("2. View meal plan")
    print("3. Exit")
    print("="*50)

def search_and_add_food(meal_plan):
    """
    Search for a food and add it to the meal plan
    
    Args:
        meal_plan: The MealPlan object to add food to
    """
    # Get search query
    query = input("\nEnter food to search for: ").strip()
    
    if not query:
        print("❌ Please enter a food name!")
        return
    
    print(f"\nSearching for '{query}'...")
    
    # Search for foods
    results = search_food(query, max_results=5)
    
    if not results:
        print("❌ No foods found or API error. Try again!")
        return
    
    # Display results
    print(f"\n✓ Found {len(results)} foods:\n")
    for i, food in enumerate(results, 1):
        print(f"{i}. {food['name']}")
        print(f"   Brand: {food['brand']}\n")
    
    # Let user choose
    try:
        choice = int(input("Which food? (enter number): "))
        
        if choice < 1 or choice > len(results):
            print("❌ Invalid choice!")
            return
        
        # Get nutrition for selected food
        selected_food = results[choice - 1]
        print(f"\nGetting nutrition info for: {selected_food['name']}...")
        
        nutrition = get_food_nutrition(selected_food['fdc_id'])
        
        if not nutrition:
            print("❌ Could not get nutrition info!")
            return
        
        # Ask for servings
        servings = float(input("How many servings? (e.g., 1, 1.5, 2): "))
        
        if servings <= 0:
            print("❌ Servings must be greater than 0!")
            return
        
        # Add to meal plan
        meal_plan.add_food(nutrition, servings)
        
    except ValueError:
        print("❌ Please enter a valid number!")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main application loop"""
    print_header()
    
    # Get user info and calculate TDEE
    print("\nFirst, let's calculate your daily calorie needs...\n")
    
    # Get user input
    weight, height, age, gender, activity = get_user_input()
    
    # Calculate BMR
    bmr = calculate_bmr(weight, height, age, gender)
    
    # Get activity multiplier
    multiplier = get_activity_multiplier(activity)
    
    if multiplier:
        # Calculate TDEE
        tdee = calculate_tdee(bmr, multiplier)
        print(f"\n✓ Your daily calorie target: {tdee} kcal")
        
        # Create meal plan with this target
        meal_plan = MealPlan(tdee)
        
        # # TODO: Show menu and handle choices
        while True:
            display_menu()
            choice = input("/nChoose an option (1-3): ").strip()

            if choice == "1":
              search_and_add_food(meal_plan)



            elif choice == "2":
                meal_plan.show_summary()

            elif choice == "3":
                break
            else:
                print("❌ Invalid choice! Please enter 1, 2 or 3.")
        print("/nThank you or using Meal Master! 👋")
        
        # print(display_menu())
        
    else:
        print("Error: Invalid activity level")
        return
    
    print("\nThank you for using Meal Master!")


if __name__ == "__main__":
    main()


