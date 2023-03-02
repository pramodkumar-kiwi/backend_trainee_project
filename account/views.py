"""
view for SignupView

"""
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, SigninSerializer
from .models import User


class SignupView(viewsets.ModelViewSet):
    """
    SignupView class to register a new user
    """
    queryset = User
    serializer_class = SignupSerializer
    http_method_names = ['post']

    def get_queryset(self):
        """
        Get the queryset of User Model
        """
        return User.objects.filter()

    def create(self, request, *args, **kwargs):
        """
        creates a new requested user
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(viewsets.ViewSet):
    """
    Allow only authenticated user to signin.
    If the user is valid provide him the access and refresh token
    and save it to the database.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = SigninSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            user_token = User.objects.get(id=user.id)
            user_token.token = str(refresh.access_token)
            user_token.save()

            return Response({'access': str(refresh.access_token), 'refresh': str(refresh)})
        return Response(status=status.HTTP_400_BAD_REQUEST)
