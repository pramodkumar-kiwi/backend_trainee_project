"""
view for SignupView

"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
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

