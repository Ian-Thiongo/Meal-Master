def calculate_bmr(weight_kg, height_cm, age, gender):
    gender = gender.lower()
    
    if gender == "male":
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    
    return round(bmr, 1)

print(calculate_bmr(90,154,34,"male"))