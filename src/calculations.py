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
