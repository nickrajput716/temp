# 🍎 Smart Diet Recommendation System - Django Complete Setup

## 📁 Complete Project Structure

```
diet_recommendation_project/
│
├── diet_project/                  # Main project folder
│   ├── __init__.py
│   ├── settings.py               # ✅ Created
│   ├── urls.py                   # ✅ Created
│   ├── wsgi.py
│   └── asgi.py
│
├── diet_app/                      # Main application
│   ├── __init__.py
│   ├── models.py                 # ✅ Created
│   ├── views.py                  # ✅ Created
│   ├── forms.py                  # ✅ Created
│   ├── ml_utils.py               # ✅ Created
│   ├── admin.py                  # Need to create
│   ├── urls.py                   # Included in main urls
│   └── migrations/
│
├── templates/                     # HTML templates
│   ├── base.html                 # ✅ Created
│   ├── diet_app/
│   │   ├── home.html            # ✅ Created
│   │   ├── calculate.html       # Need to create
│   │   ├── result.html          # Need to create
│   │   ├── dashboard.html       # Need to create
│   │   ├── profile.html         # Need to create
│   │   ├── history.html         # Need to create
│   │   └── add_weight.html      # Need to create
│   └── registration/
│       ├── login.html           # Need to create
│       └── register.html        # Need to create
│
├── static/                       # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                        # User uploaded files
│
├── ml_models/                    # ML model files
│   ├── bmi_classifier.pkl
│   ├── tdee_regressor.pkl
│   ├── label_encoder_category.pkl
│   └── label_encoder_gender.pkl
│
├── datasets/                     # Downloaded Kaggle datasets
│   ├── bmi.csv
│   ├── ObesityDataSet.csv
│   └── nutrition.csv
│
├── ml_training/                  # ML training scripts
│   └── train_models.py
│
├── requirements.txt              # Python dependencies
├── manage.py                     # Django management
└── README.md                     # This file
```

---

## 🚀 Step-by-Step Setup Instructions

### Step 1: Create Django Project

```bash
# Create project directory
mkdir diet_recommendation_project
cd diet_recommendation_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Django
pip install django

# Create Django project
django-admin startproject diet_project .

# Create Django app
python manage.py startapp diet_app
```

### Step 2: Install Dependencies

Create `requirements.txt`:
```txt
Django==4.2.7
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.2
pickle-mixin==1.0.2
Pillow==10.1.0
```

Install:
```bash
pip install -r requirements.txt
```

### Step 3: Project Configuration

Replace `diet_project/settings.py` with the provided settings file.

Key configurations:
- Added `diet_app` to `INSTALLED_APPS`
- Configured templates directory
- Set up static and media files
- Added ML models directory path

### Step 4: Create Database Models

Copy `models.py` to `diet_app/models.py`

Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Admin Interface

Create `diet_app/admin.py`:

```python
from django.contrib import admin
from .models import UserProfile, DietRecommendation, WeightLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'weight', 'height', 'diet_type', 'goal']
    list_filter = ['gender', 'diet_type', 'goal', 'activity_level']
    search_fields = ['user__username', 'user__email']

@admin.register(DietRecommendation)
class DietRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'bmi_category', 'bmi', 'recommended_calories', 'created_at']
    list_filter = ['bmi_category', 'diet_type', 'created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'

@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'date']
    list_filter = ['date']
    search_fields = ['user__username']
    date_hierarchy = 'date'
```

Create superuser:
```bash
python manage.py createsuperuser
```

### Step 6: Setup Templates

Create directories:
```bash
mkdir templates
mkdir templates/diet_app
mkdir templates/registration
```

Copy all provided HTML files to respective directories.

### Step 7: Download Kaggle Datasets

1. Go to Kaggle.com and create account
2. Download these datasets:
   - BMI Dataset: https://www.kaggle.com/datasets/yasserh/bmidataset
   - Obesity Levels: https://www.kaggle.com/datasets/ankurbajaj9/obesity-levels
   - Food Nutrition: https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset

3. Place CSV files in `datasets/` folder

### Step 8: Train ML Models

Create `ml_training/train_models.py` (use provided Python ML script)

Run training:
```bash
python ml_training/train_models.py
```

This will generate model files in `ml_models/` directory.

### Step 9: Configure URLs

Copy provided `urls.py` to `diet_project/urls.py`

### Step 10: Create Views & Forms

Copy provided files:
- `views.py` to `diet_app/views.py`
- `forms.py` to `diet_app/forms.py`
- `ml_utils.py` to `diet_app/ml_utils.py`

### Step 11: Collect Static Files

```bash
python manage.py collectstatic
```

### Step 12: Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## 📝 Additional Templates to Create

### calculate.html
```html
{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-body p-5">
                <h2 class="text-center mb-4">
                    <i class="fas fa-calculator"></i> Calculate Your Diet Plan
                </h2>
                
                <form method="POST">
                    {% csrf_token %}
                    
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Age *</label>
                            <input type="number" name="age" class="form-control" required min="10" max="100">
                        </div>
                        
                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Gender *</label>
                            <select name="gender" class="form-control" required>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                            </select>
                        </div>
                        
                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Height (cm) *</label>
                            <input type="number" name="height" class="form-control" required min="100" max="250">
                        </div>
                        
                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Weight (kg) *</label>
                            <input type="number" name="weight" class="form-control" required min="30" max="200">
                        </div>
                        
                        <div class="col-12">
                            <label class="form-label fw-semibold">Activity Level *</label>
                            <select name="activity_level" class="form-control" required>
                                <option value="sedentary">Sedentary (little/no exercise)</option>
                                <option value="light">Lightly Active (1-3 days/week)</option>
                                <option value="moderate" selected>Moderately Active (3-5 days/week)</option>
                                <option value="veryActive">Very Active (6-7 days/week)</option>
                            </select>
                        </div>
                        
                        <div class="col-12">
                            <label class="form-label fw-semibold">Your Goal *</label>
                            <select name="goal" class="form-control" required>
                                <option value="lose">Lose Weight</option>
                                <option value="maintain" selected>Maintain Weight</option>
                                <option value="gain">Gain Weight</option>
                            </select>
                        </div>
                        
                        <div class="col-12">
                            <label class="form-label fw-semibold">Diet Preference *</label>
                            <div class="btn-group w-100" role="group">
                                <input type="radio" class="btn-check" name="diet_type" id="veg" value="veg" checked>
                                <label class="btn btn-outline-success" for="veg">
                                    <i class="fas fa-leaf"></i> Vegetarian
                                </label>
                                
                                <input type="radio" class="btn-check" name="diet_type" id="nonveg" value="nonveg">
                                <label class="btn btn-outline-danger" for="nonveg">
                                    <i class="fas fa-drumstick-bite"></i> Non-Veg
                                </label>
                                
                                <input type="radio" class="btn-check" name="diet_type" id="vegan" value="vegan">
                                <label class="btn btn-outline-primary" for="vegan">
                                    <i class="fas fa-seedling"></i> Vegan
                                </label>
                            </div>
                        </div>
                        
                        <div class="col-12 mt-4">
                            <button type="submit" class="btn btn-primary w-100 btn-lg">
                                <i class="fas fa-magic"></i> Generate My Diet Plan
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### result.html
```html
{% extends 'base.html' %}
{% block content %}
<div class="row">
    <!-- Health Metrics -->
    <div class="col-lg-4 mb-4">
        <div class="card">
            <div class="card-body">
                <h4 class="mb-4"><i class="fas fa-chart-pie"></i> Your Metrics</h4>
                
                <div class="metric-box">
                    <h3>{{ result.bmi }}</h3>
                    <p>BMI</p>
                </div>
                
                <div class="alert alert-info">
                    <strong>Category:</strong>
                    <span class="badge-category {{ result.category|lower }}">
                        {{ result.category }}
                    </span>
                </div>
                
                <div class="alert alert-warning">
                    <strong>Diet Type:</strong>
                    <span class="diet-badge diet-{{ result.diet_type }}">
                        {{ result.diet_type|title }}
                    </span>
                </div>
                
                <hr>
                
                <p><strong>Base Calories (TDEE):</strong><br>
                    <span class="fs-4 text-primary">{{ result.tdee }} kcal</span>
                </p>
                
                <p><strong>Recommended Daily:</strong><br>
                    <span class="fs-4 text-success">{{ result.recommended_calories }} kcal</span>
                </p>
            </div>
        </div>
    </div>
    
    <!-- Diet Plan -->
    <div class="col-lg-8">
        <div class="card mb-4">
            <div class="card-body">
                <h4 class="mb-4">
                    <i class="fas fa-utensils"></i> {{ result.diet_plan.title }}
                </h4>
                
                <h5 class="mt-4 mb-3">Daily Meal Plan:</h5>
                {% for meal in result.diet_plan.meals %}
                <div class="meal-card">
                    {{ meal }}
                </div>
                {% endfor %}
                
                <h5 class="mt-4 mb-3">Important Tips:</h5>
                {% for tip in result.diet_plan.tips %}
                <div class="tip-card">
                    <i class="fas fa-check-circle text-primary"></i> {{ tip }}
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="text-center">
            <a href="{% url 'calculate_diet' %}" class="btn btn-outline-primary">
                <i class="fas fa-redo"></i> Calculate Again
            </a>
            {% if user.is_authenticated %}
            <a href="{% url 'dashboard' %}" class="btn btn-primary">
                <i class="fas fa-tachometer-alt"></i> Go to Dashboard
            </a>
            {% else %}
            <a href="{% url 'register' %}" class="btn btn-success">
                <i class="fas fa-user-plus"></i> Register to Save
            </a>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

---

## 🎯 Features Implemented

### ✅ Core Features:
1. **BMI Calculation** - Accurate body mass index
2. **TDEE Calculation** - Total daily energy expenditure
3. **12 Diet Plans** - Veg/Non-Veg/Vegan for each BMI category
4. **User Authentication** - Register, login, logout
5. **User Dashboard** - View history and progress
6. **Weight Tracking** - Log weight over time
7. **ML Predictions** - Random Forest models
8. **Beautiful UI** - Bootstrap 5 with gradients
9. **Responsive Design** - Mobile-friendly
10. **Admin Panel** - Manage users and data

### 🔜 Future Enhancements:
- PDF report generation
- Email notifications
- Social media sharing
- Exercise recommendations
- Nutrition calculator
- Mobile app (Flutter/React Native)
- Multi-language support
- Payment integration for premium features

---

## 🐛 Troubleshooting

### Issue: Models not loading
**Solution**: Ensure ML model files are in `ml_models/` directory

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic`

### Issue: Template not found
**Solution**: Check `TEMPLATES` configuration in settings.py

### Issue: Database errors
**Solution**: Delete db.sqlite3 and run migrations again

---

## 📊 Testing

```bash
# Run tests
python manage.py test

# Check for issues
python manage.py check

# Create test data
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('testuser', 'test@example.com', 'password123')
```

---

## 🚀 Deployment

### Heroku Deployment:
```bash
pip install gunicorn dj-database-url psycopg2
echo "web: gunicorn diet_project.wsgi" > Procfile
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### PythonAnywhere:
1. Upload code
2. Create virtual environment
3. Configure WSGI file
4. Set static files path
5. Reload web app

---

## 📧 Support

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Stack Overflow: https://stackoverflow.com/questions/tagged/django
- Create GitHub issue

---

## 📄 License

MIT License - Free to use for personal and commercial projects

---

## 👨‍💻 Author

Created with ❤️ using Django and Machine Learning

**Happy Coding! 🚀**
