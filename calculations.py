from datetime import date
# Basic calculations for phased app 
# Takes weight (kg), height (cm), age
# Returns BMR as a float
def calculate_bmr(weight, height, age, lbs, inches):
    if lbs: 
        weight /= 2.205
    if inches: 
        height *= 2.54

    bmr = (10 * weight) + (height * 6.25) - (5 * age) - 161
    return round(bmr,1)

# Takes BMR and activity level string
# Returns TDEE as a float
# use numbers from the PAL system
def calculate_tdee(bmr, activity_level):
    levels = {"sedentary": 1.2,
              "lightly active": 1.375,
              "moderately active": 1.55,
              "very active": 1.725,}
    tdee = bmr * levels[activity_level]

    return round(tdee,1)
    

# Takes last period date and cycle length
# Returns current phase as a string
def get_current_phase(last_period_date, cycle_length=28):
    today = date.today()

    current = (today - last_period_date).days

    if 0 <= current <= 4: 
        phase = "Menstrual"
    elif 5 <= current <= 13: 
        phase = "Follicular"
    elif 14 <= current <= 16: 
        phase = "Ovulation"
    elif 17 <= current <= cycle_length:
        phase = "Luteal"
    else:
        phase = "Unknown"

    return phase 

# Takes TDEE and current phase
# Returns adjusted calorie target
def adjust_calories(tdee, phase, deficit=250):
    if phase == "follicular": 
        return round(tdee - deficit, 1)
    elif phase == "luteal":
        return round(tdee + 200, 1)
    else:
        return round(tdee,1)
    