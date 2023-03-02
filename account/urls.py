"""
account URL Configuration
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('Signup', views.SignupView, basename='signup')
urlpatterns = [
    path('', include(router.urls)),
]