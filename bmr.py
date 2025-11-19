#Calculating basal metabolic rate
def calculate_bmr(weight_kg, height_cm, age, gender,):
    gender = gender.lower()
    
    if gender == "male":
        bmr =(10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) -161
    
    return round(bmr, 1)


def calculate_tdee(bmr,activity_level):
    tdee = (bmr * activity_level)

    return tdee

bmr = calculate_bmr(90,154,34,"male")
tdee = calculate_tdee(bmr, 1.55)
    
# print(f"BMR: {bmr}, TDEE: {tdee}")

def get_activity_multiplier(activity_level):

    activity_levels = {
    "sedentary": 1.2,
    "lightly_active": 1.375,
    "moderately_active": 1.55,
    "very_active": 1.725,
    "extra_active": 1.9
}

 




