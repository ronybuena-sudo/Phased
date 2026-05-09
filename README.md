# Phased 
A calorie tracker application made for women. Most calories apps ignore hormonal changes in women, which heavily impacts a woman's daily calorie intake. Phased adjusts your calorie target based on the user's menstrual cycle to show that it's not your failure, but your biology.

## Features
- Menstrual cycle phase detection based on last recorded period date 
- Automatic adjusting of calorie targets based on current phase 
- A food logging feature with calorie subtraction
- Manual macro tracking (proteins, carbs and fats)
- A food history for quick food logging 
- Multi-page onboarding to adjust calories based on user's body 
- Settings page to update data 

## Tech Stack
### Frontend
- HTML 
- CSS

### Backend
- Python 
- Flask

### Calculations
- Mifflin-St Jeor BMR Formula
- PAL Activity Multipliers for TDEE

## Installation 
Clone the Repository: 

```bash 
git clone https://github.com/ronybuena-sudo/Phased.git 
```

Install Dependencies: 
```bash
pip install flask
```

Run: 
```bash
python app.py
```

Open browser at: http://127.0.0.1:5000

## Future Improvements
- User authentication 
- Design for mobile use 
- Nutrition API for automatic macro reports 
- Data storage with SQL 
- Progress Charts 