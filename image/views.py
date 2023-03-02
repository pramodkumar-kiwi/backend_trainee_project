# Create your views here.
from rest_framework import viewsets, status

from .messages import SUCCESS_MESSAGES
from .models import ImageGallery, Image
from .serializers import ImageGalleryCreateSerializer, ImageGalleryUpdateSerializer, ImageCreateSerializer, \
    ImageUpdateSerializer
from rest_framework.response import Response


class ImageGalleryViewSet(viewsets.ModelViewSet):
    """
    The ImageGalleryView class create a new employee for the ImageGallery model.
    """
    queryset = ImageGallery
    serializer_class = ImageGalleryCreateSerializer

    def get_serializer_class(self):
        """
        The get_serializer_class method returns a ModelSerializer of ImageGallery Model objects.
        """
        if self.action in ['list', 'create']:
            return ImageGalleryCreateSerializer
        return ImageGalleryUpdateSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Department Model objects.
        """
        return ImageGallery.objects.filter().order_by('id')

    def list(self, request, *args, **kwargs):
        """
         Returns a list of all instances of the ImageGallery model.
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a single instance of the ImageGallery model, based on the primary key (pk).
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a new instance of the ImageGallery model.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['CREATED']['SUCCESSFULLY'], 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing instance of the Department model, based on the primary key (pk).
        """
        dept = self.get_object()
        serializer = self.get_serializer(dept, data=request.data)
        if serializer.is_valid():
            serializer.update(dept, serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['UPDATED']['SUCCESSFULLY'], 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial Updates an existing instance of the ImageGallery model, based on the primary key (pk).
        """
        dept = self.get_object()
        serializer = self.get_serializer(dept, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(dept, serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['UPDATED']['SUCCESSFULLY'], 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a single instance of the ImageGallery model, based on the primary key (pk).
        """
        self.get_object().delete()
        return Response({'message': SUCCESS_MESSAGES['DELETED']['SUCCESSFULLY']})


class ImageViewSet(viewsets.ModelViewSet):
    """
    The ImageGalleryView class create a new employee for the ImageGallery model.
    """
    queryset = Image
    serializer_class = ImageCreateSerializer

    def get_serializer_class(self):
        """
        The get_serializer_class method returns a ModelSerializer of ImageGallery Model objects.
        """
        if self.action in ['list', 'create']:
            return ImageCreateSerializer
        return ImageUpdateSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Department Model objects.
        """
        return Image.objects.filter().order_by('id')

    def list(self, request, *args, **kwargs):
        """
         Returns a list of all instances of the ImageGallery model.
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a single instance of the ImageGallery model, based on the primary key (pk).
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a new instance of the ImageGallery model.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['CREATED']['SUCCESSFULLY'], 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing instance of the Department model, based on the primary key (pk).
        """
        dept = self.get_object()
        serializer = self.get_serializer(dept, data=request.data)
        if serializer.is_valid():
            serializer.update(dept, serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['UPDATED']['SUCCESSFULLY'], 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial Updates an existing instance of the ImageGallery model, based on the primary key (pk).
        """
        dept = self.get_object()
        serializer = self.get_serializer(dept, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(dept, serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['UPDATED']['SUCCESSFULLY'], 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a single instance of the ImageGallery model, based on the primary key (pk).
        """
        self.get_object().delete()
        return Response({'message': SUCCESS_MESSAGES['DELETED']['SUCCESSFULLY']})