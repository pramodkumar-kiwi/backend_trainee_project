"""
This file contains Signup, Signin, Sign-out, emailvalidator, username-validator
and userprofile serializer to perform functions that call in views.
"""

import os
import re

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.urls import reverse

from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .constants import REGEX, MAX_LENGTH, MIN_LENGTH, DIRECTORY_PATH
from .messages import SIGNUP_VALIDATION_ERROR, SIGNIN_VALIDATION_ERROR, \
    EMAIL_VALIDATOR_VALIDATION_ERROR, USERNAME_VALIDATOR_VALIDATION_ERROR, \
    TOKEN_ERROR, RESET_PASSWORD, FORGET_PASSWORD
from .utils import generate_token
from .models import User, ForgetPassword


class SignupSerializer(serializers.ModelSerializer):
    """
    serializer for Registering requested user
    """
    first_name = serializers.CharField(
        max_length=MAX_LENGTH['first_name'], min_length=MIN_LENGTH['first_name'],
        required=True, allow_blank=False, trim_whitespace=True,
        error_messages=SIGNUP_VALIDATION_ERROR['first_name']
    )
    last_name = serializers.CharField(
        max_length=MAX_LENGTH['last_name'], min_length=MIN_LENGTH['last_name'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNUP_VALIDATION_ERROR['last_name']
    )
    username = serializers.CharField(
        min_length=MIN_LENGTH['username'], max_length=MAX_LENGTH['username'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNUP_VALIDATION_ERROR['username']
    )
    email = serializers.EmailField(
        required=True, allow_blank=False,
        error_messages=SIGNUP_VALIDATION_ERROR['email']
    )
    contact = serializers.CharField(
        min_length=MIN_LENGTH['contact'], max_length=MAX_LENGTH['contact'],
        required=True, allow_blank=False,
        error_messages=SIGNUP_VALIDATION_ERROR['contact']
    )
    password = serializers.CharField(
        write_only=True, min_length=MIN_LENGTH['password'], max_length=MAX_LENGTH['password'],
        allow_blank=False, error_messages=SIGNUP_VALIDATION_ERROR['password']
    )

    @staticmethod
    def validate_first_name(value):
        """
        check that the first_name should contain only alphabets
        :param value:first_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["first_name"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['first_name']['invalid'])
        return value

    @staticmethod
    def validate_last_name(value):
        """
        check that the last_name should contain only alphabets
        :param value:last_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["last_name"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['last_name']['invalid'])
        return value

    @staticmethod
    def validate_username(value):
        """
        check that the username length is from 8 to 16 characters,
        and it is alphanumeric with at least one special character
        :param value: username
        :return: if valid return value ,else return Validation error
        """
        if not re.match(REGEX["USERNAME"], value) or not any(char.isalpha() for char in value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['username']['invalid'])
        return value

    @staticmethod
    def validate_contact(value):
        """
        check that the contact should contain only digits
        :param value:contact
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["contact"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['contact']['invalid'])
        return value

    @staticmethod
    def validate_password(value):
        """
        checks password if valid : return value,
        else : return validation error
        """
        if not re.match(REGEX["PASSWORD"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['password']['invalid'])
        return value

    # pylint: disable=too-few-public-methods
    def create(self, validated_data):
        """
        creates a user
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        directory_path = os.path.join(DIRECTORY_PATH, validated_data['username'])
        os.makedirs(directory_path)
        user.save()
        return user

    class Meta:
        """
        class Meta for SignupSerializer
        """
        model = User
        fields = ['id', 'first_name', 'last_name', 'username',
                  'email', 'contact', 'password']


class SigninSerializer(serializers.ModelSerializer):
    """
    Define a serializer for a signin view in Django
    """
    username = serializers.CharField(
        min_length=MIN_LENGTH['username'], max_length=MAX_LENGTH['username'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNIN_VALIDATION_ERROR['username']
    )
    password = serializers.CharField(
        max_length=MAX_LENGTH['password'], min_length=MIN_LENGTH['password'],
        write_only=True, required=True, trim_whitespace=False,
        error_messages=SIGNIN_VALIDATION_ERROR['password']
    )

    @staticmethod
    def validate_username(value):
        """
        check that the username length is from 8 to 16 characters,
        and it is alphanumeric with at least one special character
        :param value: username
        :return: if valid return value ,else return Validation error
        """
        if not re.match(REGEX["USERNAME"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['username']['invalid'])
        return value

    @staticmethod
    def validate_password(value):
        """
        checks password if valid : return value,
        else : return validation error
        """
        if not re.match(REGEX["PASSWORD"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['password']['invalid'])
        return value

    def validate(self, attrs):
        """
            Validate if username or password is incorrect.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(SIGNIN_VALIDATION_ERROR['invalid credentials'])

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """
        This function generate the access and refresh token
        for the authenticated user
        :param validated_data:
        :return: access and refresh token
        """
        user = validated_data['user']

        refresh = RefreshToken.for_user(user)

        user_token = User.objects.get(id=user.id)
        user_token.token = str(refresh.access_token)
        user_token.save()

        return {'access': str(refresh.access_token), 'refresh': str(refresh)}

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        class Meta for SigninSerializer
        """
        model = User
        fields = ['username', 'password']


class SignOutSerializer(serializers.Serializer):
    """
    Serializer for user logout
    It blacklisted the refresh token after
    the authenticated user is logged-out
    """
    refresh = serializers.CharField(max_length=255)

    def validate(self, attrs):
        """
        Validate the refresh token from the user
        :param attrs: refresh
        :return: attrs
        """
        try:
            token = RefreshToken(attrs['refresh'])
            token_type = token.__class__.__name__
            if token_type != 'RefreshToken':
                raise serializers.ValidationError(TOKEN_ERROR['Invalid'])
            attrs['refresh_token'] = token
        except (InvalidToken, TokenError) as e:
            raise serializers.ValidationError(str(e))
        return attrs

    def create(self, validated_data):
        """
        Override create method to add refresh token
        to blacklist
        :param validated_data: refresh
        :return: success and error message
        """
        refresh_token = self.validated_data['refresh_token']
        refresh_token.blacklist()
        return {'success': True}


class EmailValidatorSerializer(serializers.ModelSerializer):
    """
    serializer for Validating email at runtime
    """
    email = serializers.EmailField(required=True, allow_blank=False,
                                   error_messages=EMAIL_VALIDATOR_VALIDATION_ERROR['email'])

    @staticmethod
    def validate_email(value):
        """
        checks that the email exits
        :param value: email
        :return: if exists: return Validation error else return value
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(EMAIL_VALIDATOR_VALIDATION_ERROR['email']['exits'])
        return True

    def create(self, validated_data):
        return validated_data

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        class Meta for EmailValidatorSerializer
        """
        model = User
        fields = ['email']


class UsernameValidatorSerializer(serializers.ModelSerializer):
    """
    serializer for Validating username at runtime
    """
    username = serializers.CharField(
        min_length=8, max_length=16, required=True, allow_blank=False,
        trim_whitespace=False, error_messages=USERNAME_VALIDATOR_VALIDATION_ERROR['username'])

    @staticmethod
    def validate_username(value):
        """
        check that the username already exists or not
        :param value: username
        :return: if exists return Validation error ,else return value
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                USERNAME_VALIDATOR_VALIDATION_ERROR['username']['exits']
            )
        return value

    def create(self, validated_data):
        return validated_data

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        class Meta for UsernameValidatorSerializer
        """
        model = User
        fields = ['username']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    serializer for User model that return the authenticated
    user details and update them
    """
    first_name = serializers.CharField(
        max_length=MAX_LENGTH['first_name'], min_length=MIN_LENGTH['first_name'],
        required=True, allow_blank=False, trim_whitespace=True,
        error_messages=SIGNUP_VALIDATION_ERROR['first_name']
    )
    last_name = serializers.CharField(
        max_length=MAX_LENGTH['last_name'], min_length=MIN_LENGTH['last_name'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNUP_VALIDATION_ERROR['last_name']
    )
    username = serializers.CharField(
        min_length=MIN_LENGTH['username'], max_length=MAX_LENGTH['username'],
        required=True, allow_blank=False, trim_whitespace=False,
        error_messages=SIGNUP_VALIDATION_ERROR['username']
    )
    email = serializers.EmailField(
        required=True, allow_blank=False, error_messages=SIGNUP_VALIDATION_ERROR['email']
    )
    contact = serializers.CharField(
        min_length=MIN_LENGTH['contact'], max_length=MAX_LENGTH['contact'],
        required=True, allow_blank=False,
        error_messages=SIGNUP_VALIDATION_ERROR['contact']
    )
    password = serializers.CharField(
        write_only=True, min_length=MIN_LENGTH['password'], max_length=MAX_LENGTH['password'],
        allow_blank=False, error_messages=SIGNUP_VALIDATION_ERROR['password']
    )

    @staticmethod
    def validate_first_name(value):
        """
        check that the first_name should contain only alphabets
        :param value:first_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["first_name"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['first_name']['invalid'])
        return value

    @staticmethod
    def validate_last_name(value):
        """
        check that the last_name should contain only alphabets
        :param value:last_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["last_name"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['last_name']['invalid'])
        return value

    @staticmethod
    def validate_username(value):
        """
        check that the username length is from 8 to 16 characters,
        and it is alphanumeric with at least one special character
        :param value: username
        :return: if valid return value ,else return Validation error
        """
        if not re.match(REGEX["USERNAME"], value) or not any(char.isalpha() for char in value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['username']['invalid'])
        return value

    @staticmethod
    def validate_contact(value):
        """
        check that the contact should contain only digits
        :param value:contact
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["contact"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['contact']['invalid'])
        return value

    @staticmethod
    def validate_password(value):
        """
        checks password if valid : return value,
        else : return validation error
        """
        if not re.match(REGEX["PASSWORD"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['password']['invalid'])
        return make_password(value)

    def update(self, instance, validated_data):
        """
        Override update method to modify the user details
        :param instance: id
        :param validated_data: validated data
        :return: userprofile
        """

        userprofile = User.objects.filter(id=instance.id).update(**validated_data)
        old_path = os.path.join(DIRECTORY_PATH, instance.username)
        new_path = os.path.join(DIRECTORY_PATH, validated_data['username'])
        os.rename(old_path, new_path)
        return userprofile

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        class Meta for UserProfileSerializer that take first name,
        last name, username, email, contact and password fields.
        """
        model = User
        fields = ['id', 'first_name', 'last_name', 'username',
                  'email', 'contact', 'password']


class ForgetPasswordSerializer(serializers.ModelSerializer):
    """
    forget password serializer to verify the email of the user
    and send the mail to its register email.
    """
    email = serializers.EmailField()

    @staticmethod
    def validate_email(email):
        """
        Validate the user's email using Django's PasswordResetForm
        """
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(FORGET_PASSWORD['email']['email_not_exist'])

        PasswordResetForm({'email': email})

        return email

    def create(self, validated_data):
        """
        Generate a password reset token and URL for the user
        :param validated_data: email
        :return: validated data
        """
        request = self.context.get('request')
        user = User.objects.get(email=validated_data['email'])
        urlsafe_base64_encode(force_bytes(user.pk))
        token = generate_token(user)
        reset_url = request.build_absolute_uri(
            reverse('reset_password-list', kwargs={'token': token})
        )

        ForgetPassword.objects.update_or_create(
            user=user,
            forget_password_token=token,
        )
        send_mail(
            'Password Reset Request',
            f'Please follow this link to reset your password: {reset_url}',
            'projectgalleria5@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return validated_data

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Class meta to define the model and the field
        of that model.
        """
        model = User
        fields = ['email']


class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset password serializer to validate the password and if it
    is validated then save the new password with the old one in the database
    """
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(RESET_PASSWORD['password_reset']['do_not_match'])

        return attrs

    @staticmethod
    def validate_new_password(value):
        """
        checks password if valid : return value,
        else : return validation error
        """
        if not re.match(REGEX["PASSWORD"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['password']['invalid'])
        return make_password(value)

    def create(self, validated_data):
        user = self.context.get('user')
        user.set_password(validated_data['new_password'])
        user.save()

        return user
