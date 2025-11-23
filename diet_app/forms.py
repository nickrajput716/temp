"""
Django Forms for Diet Recommendation System
"""

from django import forms
from .models import UserProfile, WeightLog


class UserProfileForm(forms.ModelForm):
    """Form for user health profile"""
    
    class Meta:
        model = UserProfile
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '25',
                'min': '10',
                'max': '100'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '170',
                'min': '100',
                'max': '250',
                'step': '0.1'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '70',
                'min': '30',
                'max': '200',
                'step': '0.1'
            }),
            'activity_level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'goal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'diet_type': forms.Select(attrs={
                'class': 'form-control'
            })
        }


class WeightLogForm(forms.ModelForm):
    """Form for logging weight"""
    
    class Meta:
        model = WeightLog
        fields = ['weight', 'notes']
        widgets = {
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter weight in kg',
                'min': '30',
                'max': '200',
                'step': '0.1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional notes...',
                'rows': 3
            })
        }


class DietCalculatorForm(forms.Form):
    """Quick diet calculator form (no login required)"""
    
    age = forms.IntegerField(
        min_value=10,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '25'
        })
    )
    
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    height = forms.FloatField(
        min_value=100,
        max_value=250,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '170'
        }),
        help_text='Height in cm'
    )
    
    weight = forms.FloatField(
        min_value=30,
        max_value=200,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '70'
        }),
        help_text='Weight in kg'
    )
    
    activity_level = forms.ChoiceField(
        choices=[
            ('sedentary', 'Sedentary (little/no exercise)'),
            ('light', 'Lightly Active (1-3 days/week)'),
            ('moderate', 'Moderately Active (3-5 days/week)'),
            ('veryActive', 'Very Active (6-7 days/week)')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    goal = forms.ChoiceField(
        choices=[
            ('lose', 'Lose Weight'),
            ('maintain', 'Maintain Weight'),
            ('gain', 'Gain Weight')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    diet_type = forms.ChoiceField(
        choices=[
            ('veg', 'Vegetarian'),
            ('nonveg', 'Non-Vegetarian'),
            ('vegan', 'Vegan')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )