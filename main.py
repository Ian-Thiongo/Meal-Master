# main.py
from src.user_input import get_user_input
from src.calculations import calculate_bmr, calculate_tdee, get_activity_multiplier

# Get user data
weight, height, age, gender, activity = get_user_input()

# Calculate BMR
bmr = calculate_bmr(weight, height, age, gender)

# Get activity multiplier
multiplier = get_activity_multiplier(activity)

# Calculate and display results
if multiplier:
    tdee = calculate_tdee(bmr, multiplier)
    print(f"\n--- Your Results ---")
    print(f"\nYou entered:")
    print(f"Weight: {weight} kg")
    print(f"Height: {height} cm")
    print(f"Age: {age} years")
    print(f"Gender: {gender}")
    print(f"Activity: {activity}")
    
    print(f"\n--- Your Results ---")
    print(f"BMR: {bmr} calories/day")
    print(f"Activity Level: {activity}")
    print(f"TDEE: {tdee} calories/day")
else:
    print("Invalid activity level!")


