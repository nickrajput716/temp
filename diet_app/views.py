"""
Views for Diet Recommendation System
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import UserProfile, DietRecommendation, WeightLog
from .ml_utils import diet_predictor
from .forms import UserProfileForm, WeightLogForm


def home(request):
    """Home page with diet calculator"""
    return render(request, 'diet_app/home.html')


def calculate_diet(request):
    """Calculate diet recommendation (no login required)"""
    
    if request.method == 'POST':
        # Get form data
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        activity_level = request.POST.get('activity_level')
        goal = request.POST.get('goal')
        diet_type = request.POST.get('diet_type')
        
        # Make prediction
        result = diet_predictor.predict(
            age, gender, height, weight, 
            activity_level, goal, diet_type
        )
        
        # Save to session for display
        request.session['last_result'] = result
        
        # Save to database if user is logged in
        if request.user.is_authenticated:
            DietRecommendation.objects.create(
                user=request.user,
                bmi=result['bmi'],
                bmi_category=result['category'],
                tdee=result['tdee'],
                recommended_calories=result['recommended_calories'],
                diet_type=diet_type,
                diet_plan_title=result['diet_plan']['title'],
                meals=result['diet_plan']['meals'],
                tips=result['diet_plan']['tips']
            )
        
        return render(request, 'diet_app/result.html', {'result': result})
    
    return render(request, 'diet_app/calculate.html')


@login_required
def dashboard(request):
    """User dashboard"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    recommendations = DietRecommendation.objects.filter(user=request.user)[:5]
    weight_logs = WeightLog.objects.filter(user=request.user)[:10]
    
    context = {
        'profile': profile,
        'recommendations': recommendations,
        'weight_logs': weight_logs
    }
    
    return render(request, 'diet_app/dashboard.html', context)


@login_required
def profile(request):
    """User profile management"""
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = None
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'diet_app/profile.html', {'form': form})


@login_required
def add_weight_log(request):
    """Add weight log entry"""
    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            weight_log = form.save(commit=False)
            weight_log.user = request.user
            weight_log.save()
            messages.success(request, 'Weight log added successfully!')
            return redirect('dashboard')
    else:
        form = WeightLogForm()
    
    return render(request, 'diet_app/add_weight.html', {'form': form})


@login_required
def history(request):
    """View recommendation history"""
    recommendations = DietRecommendation.objects.filter(user=request.user)
    return render(request, 'diet_app/history.html', {'recommendations': recommendations})


@login_required
def recommendation_detail(request, pk):
    """View specific recommendation"""
    recommendation = DietRecommendation.objects.get(pk=pk, user=request.user)
    return render(request, 'diet_app/recommendation_detail.html', {'recommendation': recommendation})


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'registration/login.html')


def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


# API Endpoints for AJAX requests
@csrf_exempt
def api_calculate_diet(request):
    """API endpoint for diet calculation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            result = diet_predictor.predict(
                age=data['age'],
                gender=data['gender'],
                height=data['height'],
                weight=data['weight'],
                activity_level=data['activity_level'],
                goal=data['goal'],
                diet_type=data['diet_type']
            )
            
            return JsonResponse({'status': 'success', 'data': result})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


@login_required
def api_get_weight_logs(request):
    """API endpoint to get weight logs"""
    logs = WeightLog.objects.filter(user=request.user).values('weight', 'date')
    return JsonResponse({'status': 'success', 'data': list(logs)})