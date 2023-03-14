from django.contrib.auth import authenticate
from rest_framework import serializers
from .messages import SIGNUP_VALIDATION_ERROR, SIGNIN_VALIDATION_ERROR, EMAIL_VALIDATOR_VALIDATION_ERROR, USERNAME_VALIDATOR_VALIDATION_ERROR
from .models import User
import re
from .constants import REGEX
from django.conf import settings
import os


class SignupSerializer(serializers.ModelSerializer):
    """
    serializer for Registering requested user
    """
    first_name = serializers.CharField(max_length=20, required=True, allow_blank=False, trim_whitespace=True,
                                       error_messages=SIGNUP_VALIDATION_ERROR['first_name'])
    last_name = serializers.CharField(max_length=20, required=True, allow_blank=False, trim_whitespace=False,
                                      error_messages=SIGNUP_VALIDATION_ERROR['last_name'])
    username = serializers.CharField(min_length=8, max_length=16, required=True, allow_blank=False,
                                     trim_whitespace=False,
                                     error_messages=SIGNUP_VALIDATION_ERROR['username'])
    email = serializers.EmailField(required=True, allow_blank=False,
                                   error_messages=SIGNUP_VALIDATION_ERROR['email'])
    contact = serializers.CharField(min_length=10, max_length=10, required=True, allow_blank=False,
                                    error_messages=SIGNUP_VALIDATION_ERROR['contact'])
    password = serializers.CharField(write_only=True, min_length=8, max_length=16, allow_blank=False,
                                     error_messages=SIGNUP_VALIDATION_ERROR['password'])

    def validate_first_name(self, value):
        """
        check that the first_name should contain only alphabets
        :param value:first_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["first_name"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['first_name']['invalid'])
        return value

    def validate_last_name(self, value):
        """
        check that the last_name should contain only alphabets
        :param value:last_name
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["last_name"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['last_name']['invalid'])
        return value

    def validate_username(self, value):
        """
        check that the username length is from 8 to 16 characters,
        and it is alphanumeric with at least one special character
        :param value: username
        :return: if valid return value ,else return Validation error
        """
        if not re.match(REGEX["USERNAME"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['username']['invalid'])
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['username']['exits'])
        return value

    def validate_email(self, value):
        """
        checks that the email exits
        :param value: email
        :return: if exists: return Validation error else return value
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['email']['exits'])
        return value

    def validate_contact(self, value):
        """
        check that the contact should contain only digits
        :param value:contact
        :return:if valid return value ,else return Validation error
        """
        if not re.match(REGEX["contact"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['contact']['invalid'])
        return value

    def validate_password(self, value):
        """
        checks password if valid : return value,
        else : return validation error
        """
        if not re.match(REGEX["PASSWORD"], value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['password']['invalid'])
        return value

    def create(self, validated_data):
        """
        creates a user
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        directory_path = os.path.join(settings.MEDIA_ROOT, user.username)
        os.makedirs(directory_path)
        user.save()
        return user

    class Meta:
        """
        class Meta for SignupSerializer
        """
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'contact', 'password']


class SigninSerializer(serializers.ModelSerializer):
    """
        Define a serializer for a signin view in Django
    """
    username = serializers.CharField(min_length=8, max_length=16, required=True, allow_blank=False,
                                     trim_whitespace=False)
    password = serializers.CharField(max_length=20, min_length=8, write_only=True, required=True,
                                     trim_whitespace=False)

    def validate(self, data):
        """
            Validate if username or password is incorrect.
        """
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(SIGNIN_VALIDATION_ERROR['Invalid Credentials'])

        data['user'] = user
        return data

    class Meta:
        """
        class Meta for SigninSerializer
        """
        model = User
        fields = ['username', 'password']

class EmailValidatorSerializer(serializers.ModelSerializer):
    """
    serializer for Validating email at runtime
    """
    email = serializers.EmailField(required=True, allow_blank=False,
                                   error_messages=EMAIL_VALIDATOR_VALIDATION_ERROR['email'])

    def validate_email(self, value):
        """
        checks that the email exits
        :param value: email
        :return: if exists: return Validation error else return value
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(EMAIL_VALIDATOR_VALIDATION_ERROR['email']['exits'])
        return value

    def create(self, validated_data):
        """
        Override create method to do nothing
        """
        return User()

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
    username = serializers.CharField(min_length=8, max_length=16, required=True, allow_blank=False,
                                     trim_whitespace=False,
                                     error_messages=USERNAME_VALIDATOR_VALIDATION_ERROR['username'])

    def validate_username(self, value):
        """
        check that the username already exists or not
        :param value: username
        :return: if exists return Validation error ,else return value
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(USERNAME_VALIDATOR_VALIDATION_ERROR['username']['exits'])
        return value

    class Meta:
        """
        class Meta for UsernameValidatorSerializer
        """
        model = User
        fields = ['username']
