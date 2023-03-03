"""
account URL Configuration
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
"""
Routing for Signup and Signin
"""
router.register('Signup', views.SignupView, basename='signup')
router.register('Signin', views.SigninView, basename='signin')
router.register('EmailValidator', views.EmailValidatorView, basename='EmailValidator')
router.register('UsernameValidator', views.UsernameValidatorView, basename='UsernameValidator')
urlpatterns = [
    path('', include(router.urls)),
]
