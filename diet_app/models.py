"""
Django Models for Diet Recommendation System
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    """Extended user profile with health information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(100)])
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    height = models.FloatField(help_text='Height in cm', validators=[MinValueValidator(100)])
    weight = models.FloatField(help_text='Weight in kg', validators=[MinValueValidator(30)])
    activity_level = models.CharField(
        max_length=20,
        choices=[
            ('sedentary', 'Sedentary (little/no exercise)'),
            ('light', 'Lightly Active (1-3 days/week)'),
            ('moderate', 'Moderately Active (3-5 days/week)'),
            ('veryActive', 'Very Active (6-7 days/week)')
        ],
        default='sedentary'
    )
    goal = models.CharField(
        max_length=10,
        choices=[
            ('lose', 'Lose Weight'),
            ('maintain', 'Maintain Weight'),
            ('gain', 'Gain Weight')
        ],
        default='maintain'
    )
    diet_type = models.CharField(
        max_length=10,
        choices=[
            ('veg', 'Vegetarian'),
            ('nonveg', 'Non-Vegetarian'),
            ('vegan', 'Vegan')
        ],
        default='veg'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class DietRecommendation(models.Model):
    """Store diet recommendations for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    bmi = models.FloatField()
    bmi_category = models.CharField(max_length=20)
    tdee = models.IntegerField(help_text='Total Daily Energy Expenditure')
    recommended_calories = models.IntegerField()
    diet_type = models.CharField(max_length=10)
    diet_plan_title = models.CharField(max_length=200)
    meals = models.JSONField()  # Store meals as JSON
    tips = models.JSONField()  # Store tips as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bmi_category} - {self.created_at.date()}"

    class Meta:
        verbose_name = 'Diet Recommendation'
        verbose_name_plural = 'Diet Recommendations'
        ordering = ['-created_at']


class WeightLog(models.Model):
    """Track user weight over time"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_logs')
    weight = models.FloatField(help_text='Weight in kg')
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.weight}kg on {self.date}"

    class Meta:
        verbose_name = 'Weight Log'
        verbose_name_plural = 'Weight Logs'
        ordering = ['-date']