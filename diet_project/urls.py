"""
URL Configuration for Diet Recommendation System
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from diet_app import views

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.admin_view),
    
    # Public pages
    path('', views.home, name='home'),
    path('calculate/', views.calculate_diet, name='calculate_diet'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('recommendation/<int:pk>/', views.recommendation_detail, name='recommendation_detail'),
    
    # Weight tracking
    path('add-weight/', views.add_weight_log, name='add_weight'),
    
    # API endpoints
    path('api/calculate/', views.api_calculate_diet, name='api_calculate'),
    path('api/weight-logs/', views.api_get_weight_logs, name='api_weight_logs'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Admin customization
admin.site.site_header = "Diet Recommendation System Admin"
admin.site.site_title = "Diet Recommendation Admin"
admin.site.index_title = "Welcome to Diet Recommendation System"