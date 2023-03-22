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
router.register('signup', views.SignupView, basename='signup')
router.register('signin', views.SigninView, basename='signin')
router.register('sign_out', views.SignOutView, basename='sign_out')
router.register('emailvalidator', views.EmailValidatorView, basename='emailvalidator')
router.register('username-validator', views.UsernameValidatorView, basename='username-validator')
router.register('userprofile', views.UserProfileView, basename='userprofile')
router.register('forget_password', views.ForgotPasswordView, basename='forget_password')
router.register(
    r'reset_password/(?P<token>[^/.]+)', views.ResetPasswordViewSet, basename='reset_password'
)

urlpatterns = [
    path('', include(router.urls)),
]
