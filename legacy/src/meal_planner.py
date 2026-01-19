"""
Meal Planner Module
Purpose: To allow users to build daily meal plans and track calories
"""

from src.food_api import search_food, get_food_nutrition


class MealPlan:
    def __init__(self, tdee_target):
        """Initialize a new meal plan"""
        self.tdee_target = tdee_target
        self.meals = []

    def add_food(self, food_data, servings=1):
        """Add a food to the meal plan"""
        calories = food_data['nutrients'].get('calories', 0) * servings
        protein = food_data['nutrients'].get('protein', 0) * servings
        carbs = food_data['nutrients'].get('carbs', 0) * servings
        fats = food_data['nutrients'].get('fats', 0) * servings
        
        meal = {
            'name': food_data['name'],
            'servings': servings,
            'calories': round(calories, 1),
            'protein': round(protein, 1),
            'carbs': round(carbs, 1),
            'fats': round(fats, 1)
        }
        
        self.meals.append(meal)
        print(f"✓ Added {servings} serving(s) of {food_data['name']} ({calories} calories)")

    def get_total_calories(self):
        """Calculate total calories in the meal plan"""
        total = 0
        for meal in self.meals:
            total += meal['calories']
        return total
     
    def show_summary(self):
        """Display the meal plan summary"""
        print("\n" + "="*50)
        print("MEAL PLAN SUMMARY")
        print("="*50)
        
        if not self.meals:
            print("No foods added yet!")
            return
        
        for i, meal in enumerate(self.meals, 1):
            print(f"\n{i}. {meal['name']} ({meal['servings']} serving(s))")
            print(f"   Calories: {meal['calories']} kcal")
            print(f"   Protein: {meal['protein']}g | Carbs: {meal['carbs']}g | Fats: {meal['fats']}g")
        
        total_calories = self.get_total_calories()
        remaining = self.tdee_target - total_calories
        
        print("\n" + "="*50)
        print(f"Total Calories: {total_calories} / {self.tdee_target} kcal")
        
        if remaining > 0:
            print(f"Remaining: {remaining} kcal (under target)")
        elif remaining < 0:
            print(f"Over by: {abs(remaining)} kcal (above target)")
        else:
            print("Perfect! You hit your target exactly!")
        print("="*50)