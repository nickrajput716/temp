# diet_project/__init__.py
"""
Diet Project Package Initialization
"""

# diet_app/__init__.py
"""
Diet App Package Initialization
"""
default_app_config = 'diet_app.apps.DietAppConfig'


# diet_app/apps.py
from django.apps import AppConfig


class DietAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diet_app'
    verbose_name = 'Diet Recommendation System'