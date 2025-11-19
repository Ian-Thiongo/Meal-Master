# Calculating basal metabolic rate
def calculate_bmr(
    weight_kg,
    height_cm,
    age,
    gender,
):
    gender = gender.lower()

    if gender == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    return round(bmr, 1)


def calculate_tdee(bmr, activity_level):
    tdee = bmr * activity_level
    return tdee


def get_activity_multiplier(activity_level):
    activity_levels = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9,
    }
    activity_level = activity_level.lower()

    if activity_level not in activity_levels:
        return None
    else:
        return activity_levels[activity_level]


def get_user_input():
    while True:
        try:
            weight = float(input("Enter your weight (kg): "))
            if weight <= 0 or weight > 600:
                print("Invalid weight. Must be between 0 and 600 kg.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            height = int(input("Enter your height (cm): "))
            if height <= 40 or height > 400:
                print("Invalid height. Must be between 40 and 400 cm.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            age = int(input("Enter your age: "))
            if age < 0 or age > 150:  # FIXED: changed 'and' to 'or'
                print("Invalid age. Must be between 0 and 150.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        gender = input("Enter your gender (male/female): ").lower()
        if gender in ["male", "female"]:
            break
        print("Please enter 'male' or 'female'.")

    while True:
        activity = input(
            "Enter your level of activity (sedentary/lightly active/moderately active/very active/extra active): "
        ).lower()
        if activity in [
            "sedentary",
            "lightly active",
            "moderately active",
            "very active",
            "extra active",
        ]:  
            break
        print("Please enter a valid activity level.")

    return weight, height, age, gender, activity


weight, height, age, gender, activity = get_user_input()

bmr = calculate_bmr(weight, height, age, gender)
multiplier = get_activity_multiplier(activity)

if multiplier:
    tdee = calculate_tdee(bmr, multiplier)
    print(f"\nYou entered:")
    print(f"Weight: {weight} kg")
    print(f"Height: {height} cm")
    print(f"Age: {age} years")
    print(f"Gender: {gender}")
    print(f"Activity: {activity}")
   
else:
    print("Invalid activity level!")


print(f"\n--- Your Results ---")
print(f"BMR: {bmr} calories/day")
print(f"Activity Level: {activity}")
print(f"TDEE: {round(tdee, 1)} calories/day")