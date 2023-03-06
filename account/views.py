"""
view for SignupView

"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import SignupSerializer, SigninSerializer, UsernameValidatorSerializer,\
                    EmailValidatorSerializer, SignOutSerializer
from .models import User


class SignupView(viewsets.ModelViewSet):
    """
    SignupView class to register a new user
    """
    queryset = User
    serializer_class = SignupSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        creates a new requested user
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(viewsets.ModelViewSet):
    """
    Allow only authenticated user to signin.
    If the user is valid provide him the access and refresh token
    and save it to the database.
    """
    queryset = User.objects.filter()
    serializer_class = SigninSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.create(serializer.validated_data)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(viewsets.ViewSet):
    serializer_class = SignOutSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.create(serializer.validated_data)
        return Response(data, status=status.HTTP_200_OK)


class EmailValidatorView(viewsets.ModelViewSet):
    """
    ValidateView class to Validate email at runtime
    """
    queryset = User
    serializer_class = EmailValidatorSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        """
        get queryset of User Model
        """
        return User.objects.filter(email="email")

    def retrieve(self, request, *args, **kwargs):
        """
        get an instance of user and validate it using serializer class
        """
        serializer = self.serializer_class(data=request.GET)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UsernameValidatorView(viewsets.ModelViewSet):
    """
    UsernameValidatorView class to Validate username at runtime
    """
    queryset = User.objects.filter(username="username")
    serializer_class = UsernameValidatorSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        """
        get queryset of User Model
        """
        return User.objects.filter(username="username")

    def retrieve(self, request, *args, **kwargs):
        """
        get an instance of user and validate it using serializer class
        """
        serializer = self.serializer_class(data=request.GET)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
