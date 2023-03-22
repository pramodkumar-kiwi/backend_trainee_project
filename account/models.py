"""
This module defines Django model `User` representing user .
This model is associated with its respective database table specified in its `Meta` class.
"""
import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model that extends the built-in Django User model
    with additional fields for User model

    * username and email are unique
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=16, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    contact = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.username)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the database table
        for User model
        """
        db_table = 'User'


class ForgetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=255, unique=True, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.user.email)

    class Meta:
        """
        Use the Meta class to specify the database table
        for ForgetPassword model
        """
        db_table = 'ForgetPassword'


def generate_token(user):
    """
    Generate a unique token for the given user.
    """
    token = secrets.token_hex(16)  # generate a 32-character hex string
    # associate the token with the user
    ForgetPassword.objects.update_or_create(
        user=user,
        defaults={'forget_password_token': token})
    return token
