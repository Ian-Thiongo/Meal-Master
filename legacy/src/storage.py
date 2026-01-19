"""
Storage Module
Handles saving and loading meal plans to/from JSON files
"""

import json
import os
from datetime import datetime

# Directory to store meal plans
DATA_DIR = "meal_plans"


def ensure_data_directory():
    """Create the data directory if it doesn't exist"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"✓ Created data directory: {DATA_DIR}")


def save_meal_plan(meal_plan, date=None):
    """
    Save a meal plan to a JSON file

    Args:
        meal_plan: MealPlan object to save
        date: Date string (YYYY-MM-DD). If None, uses today's date

    Returns:
        True if successful, False otherwise
    """
    ensure_data_directory()

    # Use today's date if not provided
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Create filename
    filename = os.path.join(DATA_DIR, f"{date}.json")

    # Prepare data to save
    data = {
        "date": date,
        "tdee_target": meal_plan.tdee_target,
        "meals": meal_plan.meals
    }

    # Save to file
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Meal plan saved to: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving meal plan: {e}")
        return False


def load_meal_plan(date=None):
    """
    Load a meal plan from a JSON file

    Args:
        date: Date string (YYYY-MM-DD). If None, uses today's date

    Returns:
        Dictionary with meal plan data, or None if not found
    """
    ensure_data_directory()

    # Use today's date if not provided
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Create filename
    filename = os.path.join(DATA_DIR, f"{date}.json")

    # Check if file exists
    if not os.path.exists(filename):
        return None

    # Load from file
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Error loading meal plan: {e}")
        return None


def list_saved_meal_plans():
    """
    List all saved meal plan dates

    Returns:
        List of date strings
    """
    ensure_data_directory()

    # Get all .json files
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]

    # Extract dates from filenames
    dates = [f.replace('.json', '') for f in files]
    dates.sort(reverse=True)  # Most recent first

    return dates


