
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



