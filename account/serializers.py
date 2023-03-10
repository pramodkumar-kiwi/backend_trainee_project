from django.contrib.auth import authenticate
from rest_framework import serializers
from .messages import SIGNUP_VALIDATION_ERROR, SIGNIN_VALIDATION_ERROR, EMAIL_VALIDATOR_VALIDATION_ERROR, \
    USERNAME_VALIDATOR_VALIDATION_ERROR
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
import re
from .constants import REGEX, MAX_LENGTH, MIN_LENGTH
from django.conf import settings
import os


class SignupSerializer(serializers.ModelSerializer):
    """
    serializer for Registering requested user
    """
    first_name = serializers.CharField(max_length=MAX_LENGTH['first_name'], min_length=MIN_LENGTH['first_name'],
                                       required=True, allow_blank=False, trim_whitespace=True,
                                       error_messages=SIGNUP_VALIDATION_ERROR['first_name'])
    last_name = serializers.CharField(max_length=MAX_LENGTH['last_name'], min_length=MIN_LENGTH['last_name'],
                                      required=True, allow_blank=False, trim_whitespace=False,
                                      error_messages=SIGNUP_VALIDATION_ERROR['last_name'])
    username = serializers.CharField(min_length=MIN_LENGTH['username'], max_length=MAX_LENGTH['username'],
                                     required=True, allow_blank=False, trim_whitespace=False,
                                     error_messages=SIGNUP_VALIDATION_ERROR['username'])
    email = serializers.EmailField(required=True, allow_blank=False,
                                   error_messages=SIGNUP_VALIDATION_ERROR['email'])
    contact = serializers.CharField(min_length=MIN_LENGTH['contact'], max_length=MAX_LENGTH['contact'],
                                    required=True, allow_blank=False, error_messages=SIGNUP_VALIDATION_ERROR['contact'])
    password = serializers.CharField(write_only=True, min_length=MIN_LENGTH['password'],
                                     max_length=MAX_LENGTH['password'], allow_blank=False,
                                     error_messages=SIGNUP_VALIDATION_ERROR['password'])

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
    username = serializers.CharField(min_length=MIN_LENGTH['username'], max_length=MAX_LENGTH['username'],
                                     required=True, allow_blank=False, trim_whitespace=False,
                                     error_messages=SIGNIN_VALIDATION_ERROR['username'])
    password = serializers.CharField(max_length=MAX_LENGTH['password'], min_length=MIN_LENGTH['password'],
                                     write_only=True, required=True, trim_whitespace=False,
                                     error_messages=SIGNIN_VALIDATION_ERROR['password'])

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

    def validate(self, data):
        """
            Validate if username or password is incorrect.
        """
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(SIGNIN_VALIDATION_ERROR['invalid credentials'])

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']

        refresh = RefreshToken.for_user(user)

        user_token = User.objects.get(id=user.id)
        user_token.token = str(refresh.access_token)
        user_token.save()

        return {'access': str(refresh.access_token), 'refresh': str(refresh)}

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

    @staticmethod
    def validate_email(value):
        """
        checks that the email exits
        :param value: email
        :return: if exists: return Validation error else return value
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(EMAIL_VALIDATOR_VALIDATION_ERROR['email']['exits'])
        return value

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

    @staticmethod
    def validate_username(value):
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
