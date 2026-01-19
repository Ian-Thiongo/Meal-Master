"""
Meal Master - Complete Meal Planning Application
"""

from src.user_input import get_user_input
from src.calculations import calculate_bmr, calculate_tdee, get_activity_multiplier
from src.food_api import search_food, get_food_nutrition
from src.meal_planner import MealPlan
from src.storage import save_meal_plan, load_meal_plan, list_saved_meal_plans
from datetime import datetime


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
    print("3. Save meal plan")
    print("4. Load meal plan")
    print("5. View saved meal plans")
    print("6. Exit")
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


def load_saved_meal_plan(meal_plan):
    """
    Load a previously saved meal plan
    
    Args:
        meal_plan: The current MealPlan object to load data into
    """
    # Show available dates
    dates = list_saved_meal_plans()
    
    if not dates:
        print("\n❌ No saved meal plans found!")
        return
    
    print(f"\n✓ Found {len(dates)} saved meal plans:\n")
    for i, date in enumerate(dates, 1):
        print(f"{i}. {date}")
    
    # Let user choose
    try:
        choice = input("\nEnter date (YYYY-MM-DD) or number: ").strip()
        
        # Check if they entered a number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(dates):
                date = dates[idx]
            else:
                print("❌ Invalid choice!")
                return
        else:
            date = choice
        
        # Load the meal plan
        data = load_meal_plan(date)
        
        if not data:
            print(f"❌ No meal plan found for {date}")
            return
        
        # Check if TDEE matches
        if data['tdee_target'] != meal_plan.tdee_target:
            print(f"\n⚠️  Warning: Loaded plan has different TDEE target!")
            print(f"   Current: {meal_plan.tdee_target} kcal")
            print(f"   Loaded:  {data['tdee_target']} kcal")
            
            response = input("Continue loading? (yes/no): ").lower()
            if response != 'yes':
                print("❌ Load cancelled")
                return
        
        # Clear current meals and load saved ones
        meal_plan.meals = data['meals']
        print(f"\n✓ Loaded meal plan from {date}")
        print(f"✓ Loaded {len(data['meals'])} meal(s)")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def view_saved_meal_plans():
    """Display all saved meal plans"""
    dates = list_saved_meal_plans()
    
    if not dates:
        print("\n❌ No saved meal plans found!")
        return
    
    print(f"\n✓ Found {len(dates)} saved meal plans:\n")
    
    for date in dates:
        data = load_meal_plan(date)
        if data:
            total_cals = sum(meal['calories'] for meal in data['meals'])
            print(f"📅 {date}")
            print(f"   Target: {data['tdee_target']} kcal")
            print(f"   Consumed: {total_cals} kcal")
            print(f"   Meals: {len(data['meals'])}\n")


def main():
    """Main application loop"""
    print_header()
    
    # Get user info and calculate TDEE
    print("\nFirst, let's calculate your daily calorie needs...\n")
    
    weight, height, age, gender, activity = get_user_input()
    bmr = calculate_bmr(weight, height, age, gender)
    multiplier = get_activity_multiplier(activity)
    
    if not multiplier:
        print("Error: Invalid activity level")
        return
    
    tdee = calculate_tdee(bmr, multiplier)
    print(f"\n✓ Your daily calorie target: {tdee} kcal")
    
    # Create meal plan
    meal_plan = MealPlan(tdee)
    
    # Main menu loop
    while True:
        display_menu()
        choice = input("\nChoose an option (1-6): ").strip()
        
        if choice == "1":
            search_and_add_food(meal_plan)
            
        elif choice == "2":
            meal_plan.show_summary()
            
        elif choice == "3":
            # Save meal plan
            if meal_plan.meals:
                date = datetime.now().strftime("%Y-%m-%d")
                if save_meal_plan(meal_plan, date):
                    print(f"✓ Saved meal plan for {date}")
            else:
                print("❌ No meals to save! Add some foods first.")
        
        elif choice == "4":
            # Load meal plan
            load_saved_meal_plan(meal_plan)
            
        elif choice == "5":
            # View saved meal plans
            view_saved_meal_plans()
            
        elif choice == "6":
            # Exit
            break
            
        else:
            print("❌ Invalid choice! Please enter 1-6.")
    
    print("\nThank you for using Meal Master! 👋")


if __name__ == "__main__":
    main()