def calculate_bmr(weight_kg, height_cm, age, gender):
    gender = gender.lower()
    
    if gender == "male":
        bmr =(10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) -161
    
    return round(bmr, 1)

