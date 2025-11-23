"""
Machine Learning Utilities for Diet Recommendation
"""

import pickle
import numpy as np
from pathlib import Path
from django.conf import settings

class DietPredictor:
    """Handle ML predictions and calculations"""
    
    def __init__(self):
        self.models_loaded = False
        self.bmi_model = None
        self.tdee_model = None
        self.le_category = None
        self.le_gender = None
        
    def load_models(self):
        """Load trained ML models"""
        try:
            models_dir = settings.ML_MODELS_DIR
            self.bmi_model = pickle.load(open(models_dir / 'bmi_classifier.pkl', 'rb'))
            self.tdee_model = pickle.load(open(models_dir / 'tdee_regressor.pkl', 'rb'))
            self.le_category = pickle.load(open(models_dir / 'label_encoder_category.pkl', 'rb'))
            self.le_gender = pickle.load(open(models_dir / 'label_encoder_gender.pkl', 'rb'))
            self.models_loaded = True
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    @staticmethod
    def calculate_bmi(weight, height):
        """Calculate BMI"""
        height_m = height / 100
        return weight / (height_m ** 2)
    
    @staticmethod
    def get_bmi_category(bmi):
        """Get BMI category"""
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Healthy'
        elif bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
    
    @staticmethod
    def calculate_tdee(weight, height, age, gender, activity_level):
        """Calculate Total Daily Energy Expenditure"""
        # Harris-Benedict equation
        s = 5 if gender.lower() == 'male' else -161
        bmr = 10 * weight + 6.25 * height - 5 * age + s
        
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'veryActive': 1.725
        }
        
        return bmr * activity_multipliers.get(activity_level, 1.55)
    
    @staticmethod
    def adjust_calories_for_goal(tdee, goal):
        """Adjust calories based on user goal"""
        if goal == 'lose':
            return tdee - 400
        elif goal == 'gain':
            return tdee + 400
        return tdee
    
    @staticmethod
    def get_diet_plan(category, goal, diet_type):
        """Get diet plan based on category and type"""
        
        plans = {
            'Underweight': {
                'veg': {
                    'title': "High-Calorie Vegetarian Diet",
                    'meals': [
                        "🌅 Breakfast: Paneer paratha + milk + almonds + banana",
                        "🍽️ Mid-Morning: Peanut butter sandwich + mango smoothie",
                        "🍛 Lunch: Rice + dal makhani + mixed veg curry + curd + ghee roti",
                        "☕ Evening: Dry fruits (cashews, walnuts) + cheese cubes + fruit juice",
                        "🌙 Dinner: 3 roti + paneer butter masala + raita + kheer"
                    ],
                    'tips': [
                        "Eat every 2-3 hours",
                        "Add ghee/butter to all meals",
                        "Include paneer, tofu in every meal",
                        "Consume nuts and dairy products regularly"
                    ]
                },
                'nonveg': {
                    'title': "High-Calorie Non-Vegetarian Diet",
                    'meals': [
                        "🌅 Breakfast: Egg bhurji (3 eggs) + bread + milk + banana",
                        "🍽️ Mid-Morning: Chicken sandwich + protein shake",
                        "🍛 Lunch: Rice + chicken curry + dal + egg + curd + ghee roti",
                        "☕ Evening: Dry fruits + boiled eggs (2) + smoothie",
                        "🌙 Dinner: 3 roti + butter chicken + fish fry + raita"
                    ],
                    'tips': [
                        "Include eggs in breakfast daily",
                        "Eat lean meats (chicken, fish) twice daily",
                        "Add protein supplements if needed",
                        "Consume calorie-dense non-veg items"
                    ]
                },
                'vegan': {
                    'title': "High-Calorie Vegan Diet",
                    'meals': [
                        "🌅 Breakfast: Tofu scramble + avocado toast + almond milk + banana",
                        "🍽️ Mid-Morning: Peanut butter + apple + vegan protein shake",
                        "🍛 Lunch: Brown rice + chickpea curry + tofu + mixed dal + tahini",
                        "☕ Evening: Mixed nuts + hummus + dates + coconut milk smoothie",
                        "🌙 Dinner: Quinoa + lentil curry + roasted vegetables + flax seeds"
                    ],
                    'tips': [
                        "Use plant-based protein sources (tofu, tempeh, legumes)",
                        "Add nuts, seeds, and nut butters liberally",
                        "Include avocado and coconut products",
                        "Consider vegan protein supplements"
                    ]
                }
            },
            'Healthy': {
                'veg': {
                    'title': "Balanced Vegetarian Diet",
                    'meals': [
                        "🌅 Breakfast: Oats/poha + fruits + paneer + green tea",
                        "🍽️ Mid-Morning: Curd + handful of almonds",
                        "🍛 Lunch: 2 roti + dal + mixed veg + salad + curd",
                        "☕ Evening: Sprouts chat + green tea + fruit",
                        "🌙 Dinner: Soup + 2 chapati + paneer curry + cucumber salad"
                    ],
                    'tips': [
                        "Maintain regular meal times",
                        "Include variety of vegetables and pulses",
                        "Stay hydrated (8-10 glasses water)",
                        "Exercise 30 mins daily"
                    ]
                },
                'nonveg': {
                    'title': "Balanced Non-Vegetarian Diet",
                    'meals': [
                        "🌅 Breakfast: Boiled eggs (2) + oats + fruits + milk",
                        "🍽️ Mid-Morning: Yogurt + nuts + banana",
                        "🍛 Lunch: 2 roti + chicken/fish curry + dal + salad",
                        "☕ Evening: Boiled egg + fruit + green tea",
                        "🌙 Dinner: Soup + 2 chapati + grilled chicken + vegetables"
                    ],
                    'tips': [
                        "Include lean protein in every meal",
                        "Eat fish 2-3 times per week",
                        "Balance with plenty of vegetables",
                        "Regular exercise essential"
                    ]
                },
                'vegan': {
                    'title': "Balanced Vegan Diet",
                    'meals': [
                        "🌅 Breakfast: Oatmeal + berries + chia seeds + almond milk",
                        "🍽️ Mid-Morning: Apple + walnuts + vegan yogurt",
                        "🍛 Lunch: Quinoa + chickpea curry + mixed vegetables + tahini",
                        "☕ Evening: Hummus + carrot sticks + green tea",
                        "🌙 Dinner: Lentil soup + whole grain bread + roasted tofu + salad"
                    ],
                    'tips': [
                        "Ensure B12 supplementation",
                        "Combine legumes with grains for complete protein",
                        "Include variety of plant-based proteins",
                        "Eat rainbow of vegetables daily"
                    ]
                }
            },
            'Overweight': {
                'veg': {
                    'title': "Calorie-Controlled Vegetarian Diet",
                    'meals': [
                        "🌅 Breakfast: Green tea + moong dal cheela + 1 fruit",
                        "🍽️ Mid-Morning: Apple/orange + 5 almonds",
                        "🍛 Lunch: Brown rice (small) + dal + lots of salad + curd",
                        "☕ Evening: Roasted chana + green tea + cucumber",
                        "🌙 Dinner: Vegetable soup + 1 roti + steamed vegetables"
                    ],
                    'tips': [
                        "Avoid fried foods and sweets",
                        "Cut refined carbs and sugar",
                        "Eat smaller, frequent meals",
                        "Walk 45 mins daily"
                    ]
                },
                'nonveg': {
                    'title': "Calorie-Controlled Non-Vegetarian Diet",
                    'meals': [
                        "🌅 Breakfast: Green tea + egg white omelette (3 whites) + 1 toast",
                        "🍽️ Mid-Morning: Apple + handful of nuts",
                        "🍛 Lunch: Brown rice (small) + grilled chicken breast + salad",
                        "☕ Evening: Boiled eggs (whites only) + green tea",
                        "🌙 Dinner: Clear soup + grilled fish + steamed vegetables"
                    ],
                    'tips': [
                        "Choose lean proteins (chicken breast, fish)",
                        "Avoid red meat and fried items",
                        "No sugar, no processed foods",
                        "Cardio exercise 45 mins daily"
                    ]
                },
                'vegan': {
                    'title': "Calorie-Controlled Vegan Diet",
                    'meals': [
                        "🌅 Breakfast: Green tea + tofu scramble + spinach + tomato",
                        "🍽️ Mid-Morning: Orange + 8 almonds",
                        "🍛 Lunch: Quinoa (small portion) + lentil curry + large salad",
                        "☕ Evening: Carrot sticks + hummus + green tea",
                        "🌙 Dinner: Vegetable soup + steamed broccoli + baked tofu"
                    ],
                    'tips': [
                        "Focus on low-calorie, high-volume foods",
                        "Avoid vegan junk foods and oils",
                        "Include plenty of leafy greens",
                        "Stay active throughout the day"
                    ]
                }
            },
            'Obese': {
                'veg': {
                    'title': "Intensive Weight Loss Vegetarian Diet",
                    'meals': [
                        "🌅 Breakfast: High protein - moong dal sprouts + green tea",
                        "🍽️ Mid-Morning: Cucumber/carrot sticks only",
                        "🍛 Lunch: Large salad bowl + 1 small roti + dal (no rice)",
                        "☕ Evening: Herbal tea + roasted chana (small handful)",
                        "🌙 Dinner: Clear vegetable soup + steamed vegetables"
                    ],
                    'tips': [
                        "Eliminate all sugar, sweets, fried foods",
                        "Consider intermittent fasting (16:8)",
                        "Drink 2 glasses water before meals",
                        "Cardio exercise 60 mins daily",
                        "Consult a nutritionist"
                    ]
                },
                'nonveg': {
                    'title': "Intensive Weight Loss Non-Vegetarian Diet",
                    'meals': [
                        "🌅 Breakfast: Egg whites (4-5) + spinach + black coffee",
                        "🍽️ Mid-Morning: Cucumber only",
                        "🍛 Lunch: Large salad + grilled chicken breast (100g) + lemon",
                        "☕ Evening: Green tea + carrot sticks",
                        "🌙 Dinner: Clear soup + grilled fish + steamed broccoli"
                    ],
                    'tips': [
                        "Only lean proteins - chicken breast, fish",
                        "Zero sugar, zero fried foods",
                        "High protein, very low carb approach",
                        "Intensive exercise 60+ mins daily",
                        "Medical supervision recommended"
                    ]
                },
                'vegan': {
                    'title': "Intensive Weight Loss Vegan Diet",
                    'meals': [
                        "🌅 Breakfast: Tofu scramble + spinach + black coffee",
                        "🍽️ Mid-Morning: Celery sticks only",
                        "🍛 Lunch: Large raw salad + baked tofu (small) + lemon",
                        "☕ Evening: Herbal tea + cucumber slices",
                        "🌙 Dinner: Vegetable broth + steamed greens + small portion legumes"
                    ],
                    'tips': [
                        "Whole food plant-based approach",
                        "Eliminate all processed vegan foods",
                        "High fiber, low calorie density",
                        "Intensive daily exercise required",
                        "Professional guidance essential"
                    ]
                }
            }
        }
        
        return plans.get(category, {}).get(diet_type, plans['Healthy']['veg'])
    
    def predict(self, age, gender, height, weight, activity_level, goal, diet_type):
        """Make complete prediction"""
        
        # Calculate BMI
        bmi = self.calculate_bmi(weight, height)
        category = self.get_bmi_category(bmi)
        
        # Calculate TDEE
        tdee = self.calculate_tdee(weight, height, age, gender, activity_level)
        
        # Adjust for goal
        recommended_calories = self.adjust_calories_for_goal(tdee, goal)
        
        # Get diet plan
        diet_plan = self.get_diet_plan(category, goal, diet_type)
        
        return {
            'bmi': round(bmi, 1),
            'category': category,
            'tdee': round(tdee),
            'recommended_calories': round(recommended_calories),
            'diet_plan': diet_plan,
            'diet_type': diet_type
        }


# Create global instance
diet_predictor = DietPredictor()