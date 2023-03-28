"""
This file contains different ViewSets for 'Image' and 'ImageGallery'
The ImageGalleryViewSet handles CRUD operations for the ImageGallery model,
which represents a collection of images.
The ImageViewSet handles create and delete operations for the Image model,
which represents an individual gallery.
Both ViewSet requires authentication for all actions and
provides different serializers for different actions.
The ViewSets also uses the MultiPartParser and FormParser to handle file uploads.
"""
import os
import shutil

from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from gallery.constants import MEDIA_URL, IMAGE_PATH_TEMPLATE, \
    IMAGE_GALLERY_PATH
from gallery.messages import SUCCESS_MESSAGES, VALIDATION
from gallery.models import ImageGallery, Image
from gallery.serializers import ImageGallerySerializer, ImageGalleryCreateSerializer, \
    ImageGalleryUpdateSerializer, ImageCreateSerializer, ImageSerializer


# Create your views here

# pylint: disable=too-many-ancestors
class ImageGalleryViewSet(viewsets.ModelViewSet):
    """
    The ImageGalleryViewSet handles CRUD operations for the ImageGallery model,
    with authentication required for all actions.
    It provides a serializer class for each action and
    filters queryset based on the authenticated user.
    """
    queryset = ImageGallery
    http_method_names = ['get', 'post', 'put', 'delete']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        The get_serializer_class returns a serializer class based on the action being performed.
        For 'create' action, it returns ImageGalleryCreateSerializer,
        for 'update' action, it returns ImageGalleryUpdateSerializer,
        and for all other actions, it returns the default serializer, ImageGallerySerializer.
        :return:serializer class
        """
        if self.action == 'create':
            return ImageGalleryCreateSerializer
        if self.action == 'update':
            return ImageGalleryUpdateSerializer
        return ImageGallerySerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of ImageGallery Model objects
        filtered based on the authenticated user.
        It orders the queryset based on the ID of the objects.
        :return: Image Gallery objects
        """
        user = self.request.user.id
        return ImageGallery.objects.filter(user=user).order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        The list retrieves all instances of the ImageGallery model.
        serializes them using the serializer returned by the get_serializer() method,
        and returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Image Gallery instances
        """
        if not self.get_queryset().exists():
            return Response(
                {"message": VALIDATION['image_gallery_set']['no_album']}, status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        This method retrieves a single instance of the ImageGallery model
        using the provided primary key (pk).
        It then serializes the instance using the serializer defined for the view and
        returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Single Image Gallery instance
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        This method creates a new instance of the ImageGallery model using validated serializer data
        If the data is valid, it creates a new instance and
        returns a success response with a status code of 201.
        If the data is invalid, it returns an error response with a status code of 400.
        :return: response object
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            image_gallery = serializer.create(serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['IMAGE_GALLERY']['CREATED_SUCCESSFULLY'],
                             'data': {
                                 'id': image_gallery.id,
                                 'gallery': image_gallery.gallery_name,
                                 'created_at': image_gallery.created_at,
                             }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        This method creates a new instance of the ImageGallery model using validated serializer data
        and the primary key of the instance to be updated.
        If the update is successful, it updates an existing instance and
        returns a success response with a status code of 201.
        If the update is unsuccessful, it returns an error response with a status code of 400.
        :return: response object
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            image_gallery = serializer.update(instance, serializer.validated_data)
            images = Image.objects.filter(image_gallery=image_gallery)
            updated_image_urls = []
            for image in images:
                image_url = request.build_absolute_uri(image.image.url)
                image_data = {
                    "id": image.id,
                    "image": image_url,
                    "image_gallery_id": image_gallery.id,
                    "created_at": image.created_at,
                    "updated_at": image.updated_at
                }
                updated_image_urls.append(image_data)

            return Response({'message': SUCCESS_MESSAGES['IMAGE_GALLERY']['UPDATED_SUCCESSFULLY'],
                             'data': {
                                 'id': image_gallery.id,
                                 'gallery': image_gallery.gallery_name,
                                 'images': updated_image_urls,
                                 'created_at': image_gallery.created_at,
                                 'updated_at': image_gallery.updated_at,
                             }},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        This method deletes an instance of the ImageGallery model using the primary key
        It also deletes the associated gallery folder if it exists.
        It returns a success response with a message after the deletion is complete.
        :return: success response
        """
        instance = self.get_object()
        user = request.user
        folder_path = IMAGE_GALLERY_PATH.format(
            username=user.username, gallery_name=instance.gallery_name
        )
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        instance.delete()
        return Response({'message': SUCCESS_MESSAGES['IMAGE_GALLERY']['DELETED_SUCCESSFULLY']},
                        status=status.HTTP_200_OK)


class ImageViewSet(viewsets.ModelViewSet):
    """
    The ImageViewSet handles Create and Delete operations for the ImageGallery model,
    with authentication required for all actions.
    It provides a serializer class for each action and
    filters queryset based on the authenticated user.
    """
    queryset = Image
    http_method_names = ['get', 'post', 'delete']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        """
        The get_serializer_class returns a serializer class based on the action being performed.
        For 'create' action, it returns ImageCreateSerializer,
        and for all other actions, it returns the default serializer, ImageSerializer.
        :return:serializer class
        """
        if self.action == 'create':
            return ImageCreateSerializer
        return ImageSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Image Model objects
        filtered based on the authenticated user.
        It orders the queryset based on the ID of the objects.
        :return: Image Gallery objects
        """
        user = self.request.user.id
        return Image.objects.filter(image_gallery__user=user).order_by('-id')

    def list(self, request, *args, **kwargs):
        """
        The list retrieves all instances of the Image model.
        serializes them using the serializer returned by the get_serializer() method,
        and returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Image instances
        """
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"message": VALIDATION['image']['no_image']}, status=status.HTTP_200_OK
            )
        images = []
        for image in queryset:
            serializer = self.get_serializer(image)
            images.append(serializer.data)
        return Response(images, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        This method retrieves a single instance of the Image model
        using the provided primary key (pk).
        It then serializes the instance using the serializer defined for the view and
        returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Single Image instance
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Image model
        If the data is valid, it creates a new instance and
        returns a success response with a status code of 201.
        If the data is invalid, it returns an error response with a status code of 400.
        :return: response object
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            images = serializer.create(serializer.validated_data)

            response_data = []
            for image in images:
                image_url = request.build_absolute_uri(image.image.url)
                response_data.append({
                    'id': image.id,
                    'image': image_url,
                    'image_gallery_id': image.image_gallery_id,
                    'gallery': image.image_gallery.gallery_name,
                    'created_at': image.created_at,
                    'updated_at': image.updated_at,
                })
            return Response(
                {'message': SUCCESS_MESSAGES['IMAGE']['CREATED_SUCCESSFULLY'], 'data': response_data
                 },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        This method deletes an instance of the Image model using the primary key
        It also deletes the associated gallery folder if it exists.
        It returns a success response with a message after the deletion is complete.
        :return: success response
        """
        instance = self.get_object()
        image_path = IMAGE_PATH_TEMPLATE.format(MEDIA_URL, instance.image.name)
        os.remove(image_path)
        instance.delete()
        return Response({'message': SUCCESS_MESSAGES['IMAGE']['DELETED_SUCCESSFULLY']},
                        status=status.HTTP_200_OK)
