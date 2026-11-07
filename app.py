from flask import Flask, render_template, request, session, redirect
from calculations import calculate_bmr, calculate_tdee, get_current_phase, adjust_calories

app = Flask(__name__)
app.secret_key = "phased1"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup") 
def signup():
    return render_template("signup.html")

@app.route("/onboard1", methods=["GET", "POST"])
def onboard1():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        session["age"] = request.form.get("age")
        session["height"] = request.form.get("height")
        session["height_unit"] = request.form.get("height_unit")
        session["weight"] = request.form.get("weight")
        session["weight_unit"] = request.form.get("weight_unit")
        return redirect("/onboard2")
    return render_template("onboard1.html")

@app.route("/onboard2", methods=["GET", "POST"])
def onboard2():
    if request.method == "POST":
        session["goal_weight"] = request.form.get("goal_weight")
        session["weightloss"] = request.form.get("weightloss")
        return redirect("/onboard3")
    return render_template("onboard2.html")

@app.route("/onboard3", methods=["GET", "POST"])
def onboard3():
    if request.method == "POST": 
        session["activity"] = request.form.get("activity")
        session["period"] = request.form.get("period")
        return redirect("/homepage")
    return render_template("onboard3.html")

@app.route("/foodlog", methods=["GET", "POST"])
def foodlog():
    if request.method == "POST":
        food_name = request.form.get("food_name")
        calories = request.form.get("calories")
        protein = request.form.get("protein")
        carbs = request.form.get("carbs")
        fat = request.form.get("fat")

        if "food_log" not in session: 
            session["food_log"] = []
        session["food_log"].append({"name": food_name, "calories": calories, "protein": protein, "carbs": carbs, "fat": fat})
        session.modified = True
         
        if "food_history" not in session: 
            session["food_history"] = []
        existing = [f["name"] for f in session["food_history"]]

        if food_name not in existing:
            session["food_history"].append({"name": food_name, "calories": calories, "protein": protein, "carbs": carbs, "fat": fat})

        return redirect("/homepage")
    food_history = session.get("food_history", [])
    return render_template("foodlog.html", food_history=food_history)
    
@app.route("/homepage")
def homepage():
    name = session.get("name")
    age = int(session.get("age"))
    height = float(session.get("height"))
    height_unit = session.get("height_unit")
    weight = float(session.get("weight"))
    weight_unit = session.get("weight_unit")
    goal_weight = session.get("goal_weight")
    weightloss = session.get("weightloss")
    activity = session.get("activity")
    period = session.get("period")

    pounds = weight_unit == "lbs"
    inches = height_unit == "inches"

    bmr = calculate_bmr(weight, height, age, pounds, inches)
    tdee = calculate_tdee(bmr, activity)

    from datetime import date
    last_period = date.fromisoformat(period)
    current_phase = get_current_phase(last_period)
    deficit = adjust_calories(tdee, current_phase)

    totalcal = 0
    totalpro = 0
    totalcarb = 0
    totalfat = 0
    food_log = session.get("food_log", [])
    for i in food_log: 
        totalcal += int(i.get("calories") or 0)
        totalpro += int(i.get("protein") or 0)
        totalcarb += int(i.get("carbs") or 0)
        totalfat += int(i.get("fat") or 0)
    remaining = deficit - totalcal
    target = deficit 
    cycle_day = (date.today() - last_period).days + 1
    marker = None if current_phase == "Unknown" else round((cycle_day - 0.5) / 29 * 100, 1)
    ring = round(min(max(totalcal / target, 0), 1) * 440) if target > 0 else 0
    adjustment = round(target - tdee)

    macro_total = totalpro + totalcarb + totalfat
    def share(x): 
        if macro_total: 
            return round(x / macro_total * 100)
        else: 
            return 0

    try: 
        to_go = round(abs(weight - float(goal_weight)), 1)
    except: 
        to_go = None
    
    phase_descriptions = {
        "Menstrual": "Your body is shedding its lining. Be sure to rest and eat lots of iron rich foods!",
        "Follicular": "Energy is going up! Best time to focus on your goals!",
        "Ovulation": "Peak Energy! Go reach those goals!",
        "Luteal": "Progesterone is rising! You deserve to eat a bit more, its normal!",
        "Unknown": "Track your cycle!"
    }
    descriptions = phase_descriptions.get(current_phase)

    return render_template("homepage.html", name=name, phase=current_phase, descriptions=descriptions, calories=round(remaining,1), 
                           tdee=tdee, totalpro=totalpro, totalcarb=totalcarb, totalfat=totalfat,
                           target=round(target), eaten=totalcal, ring=ring, adjustment=adjustment,
                           cycle_day=cycle_day, marker=marker,
                           pro_pct=share(totalpro), carb_pct=share(totalcarb), fat_pct=share(totalfat),
                           food_log=food_log[-6:], food_history=session.get("food_history", [])[:4],
                           weight=weight, goal_weight=goal_weight, weight_unit=weight_unit, to_go=to_go)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        if request.form.get("period"):
            session["period"] = request.form.get("period")
        if request.form.get("weight"):
            session["weight"] = request.form.get("weight")
            if request.form.get("weight_unit"):
                session["weight_unit"] = request.form.get("weight_unit")
        if request.form.get("goal_weight"):
            session["goal_weight"] = request.form.get("goal_weight")
        if request.form.get("activity"):
            session["activity"] = request.form.get("activity")
        return redirect("/homepage")
    return render_template("settings.html", period=session.get("period"), weight=session.get("weight"),
                           goal_weight=session.get("goal_weight"), weight_unit=session.get("weight_unit", "kg"),
                           activity=session.get("activity"))

if __name__ == "__main__":
    app.run(debug=True)
