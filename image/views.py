"""
This file defines Django views `ImageGalleryViewSet` and 'ImageViewSet'
representing gallery and image .
This model is associated with its respective database table specified in its `Meta` class.
"""
import os
import shutil

from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .messages import SUCCESS_MESSAGES
from .models import ImageGallery, Image
from .serializers import ImageGallerySerializer, ImageGalleryCreateSerializer, \
    ImageGalleryUpdateSerializer, ImageCreateSerializer, ImageSerializer


# Create your views here
class ImageGalleryViewSet(viewsets.ModelViewSet):
    """
    The ImageGalleryView class create a new employee for the ImageGallery model.
    """
    queryset = ImageGallery
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ImageGalleryCreateSerializer
        if self.action == 'update':
            return ImageGalleryUpdateSerializer
        return ImageGallerySerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Department Model objects.
        """
        user = self.request.user
        return ImageGallery.objects.filter(user=user).order_by('id')

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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['IMAGE_GALLERY']['CREATED_SUCCESSFULLY'],
                             'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing instance of the ImageGallery model, based on the primary key (pk).
        """
        gal = self.get_object()
        serializer = self.get_serializer(gal, data=request.data)
        if serializer.is_valid():
            serializer.update(gal, serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['IMAGE_GALLERY']['UPDATED_SUCCESSFULLY'],
                             'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a single instance of the ImageGallery model,
        based on the primary key (pk).
        """
        instance = self.get_object()
        user = request.user
        folder_path = f"media/{user.username}/image/{instance.gallery_name}"
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        instance.delete()
        return Response({'message': SUCCESS_MESSAGES['IMAGE_GALLERY']['DELETED_SUCCESSFULLY']})


class ImageViewSet(viewsets.ModelViewSet):
    """
    The ImageGalleryView class create a new employee for the ImageGallery model.
    """
    queryset = Image
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return ImageCreateSerializer
        return ImageSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Image Model objects.
        """
        user = self.request.user
        return Image.objects.filter(image_gallery__user=user).order_by('id')

    def list(self, request, *args, **kwargs):
        """
        Returns a list of all instances of the Image model.
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a single instance of the Image model,
        based on the primary key (pk).
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a new instance of the Image model.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['IMAGE']['CREATED_SUCCESSFULLY'],
                             'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a single instance of the Image model,
        based on the primary key (pk).
        """
        instance = self.get_object()
        user = request.user
        image_path = instance.image_upload_path(filename=instance.image)
        if os.path.exists(image_path):
            os.remove(image_path)
        instance.delete()
        return Response({'message': SUCCESS_MESSAGES['IMAGE']['DELETED_SUCCESSFULLY']})
