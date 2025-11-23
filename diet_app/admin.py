"""
Django Admin Configuration for Diet Recommendation System
"""

from django.contrib import admin
from .models import UserProfile, DietRecommendation, WeightLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for User Profiles"""
    list_display = ['user', 'age', 'gender', 'weight', 'height', 'bmi_display', 'diet_type', 'goal', 'created_at']
    list_filter = ['gender', 'diet_type', 'goal', 'activity_level', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Physical Attributes', {
            'fields': ('age', 'gender', 'height', 'weight')
        }),
        ('Activity & Goals', {
            'fields': ('activity_level', 'goal', 'diet_type')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def bmi_display(self, obj):
        """Calculate and display BMI"""
        height_m = obj.height / 100
        bmi = obj.weight / (height_m ** 2)
        return f"{bmi:.1f}"
    bmi_display.short_description = 'BMI'
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).select_related('user')


@admin.register(DietRecommendation)
class DietRecommendationAdmin(admin.ModelAdmin):
    """Admin interface for Diet Recommendations"""
    list_display = ['user', 'bmi_category', 'bmi', 'diet_type', 'recommended_calories', 'created_at']
    list_filter = ['bmi_category', 'diet_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'diet_plan_title']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User & Category', {
            'fields': ('user', 'bmi_category', 'bmi', 'diet_type')
        }),
        ('Calorie Information', {
            'fields': ('tdee', 'recommended_calories')
        }),
        ('Diet Plan Details', {
            'fields': ('diet_plan_title', 'meals', 'tips')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).select_related('user')


@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    """Admin interface for Weight Logs"""
    list_display = ['user', 'weight', 'date', 'has_notes']
    list_filter = ['date']
    search_fields = ['user__username', 'user__email', 'notes']
    readonly_fields = ['date']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Weight Entry', {
            'fields': ('user', 'weight', 'date')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )
    
    def has_notes(self, obj):
        """Check if notes exist"""
        return bool(obj.notes)
    has_notes.boolean = True
    has_notes.short_description = 'Has Notes'
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).select_related('user')


# Customize admin site
admin.site.site_header = "Smart Diet Recommendation Admin"
admin.site.site_title = "Diet System Admin"
admin.site.index_title = "Welcome to Diet Recommendation System Administration"