"""
This file defines Django views `BaseGalleryViewSet` which is superclass for 'ImageGalleryViewSet'
and 'VideoGalleryViewSet'
'BaseMediaViewSet' which is superclass for 'ImageViewSet' and 'VideoViewSet'
"""
import os
import shutil
from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .constants import MEDIA_URL,\
    VIDEO_PATH_TEMPLATE, VIDEO_GALLERY_PATH
from .messages import SUCCESS_MESSAGES
from .models import VideoGallery, Video
from .serializers import VideoGallerySerializer, \
    VideoGalleryCreateSerializer, VideoGalleryUpdateSerializer, \
    VideoSerializer, VideoCreateSerializer


class VideoGalleryViewSet(viewsets.ModelViewSet):
    """
    The VideoGalleryViewSet handles CRUD operations for the VideoGallery model,
    with authentication required for all actions.
    It provides a serializer class for each action and
    filters queryset based on the authenticated user.
    """
    queryset = VideoGallery
    http_method_names = ['get', 'post', 'put', 'delete']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        The get_serializer_class returns a serializer class based on the action being performed.
        For 'create' action, it returns VideoGalleryCreateSerializer,
        for 'update' action, it returns VideoGalleryUpdateSerializer,
        and for all other actions, it returns the default serializer, VideoGallerySerializer.
        :return:serializer class
        """
        if self.action == 'create':
            return VideoGalleryCreateSerializer
        if self.action == 'update':
            return VideoGalleryUpdateSerializer
        return VideoGallerySerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of VideoGallery Model objects
        filtered based on the authenticated user.
        It orders the queryset based on the ID of the objects.
        :return: Video Gallery objects
        """
        user = self.request.user
        return VideoGallery.objects.filter(user=user).order_by('id')

    def list(self, request, *args, **kwargs):
        """
        The list retrieves all instances of the VideoGallery model.
        serializes them using the serializer returned by the get_serializer() method,
        and returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Video Gallery instances
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        This method retrieves a single instance of the VideoGallery model
        using the provided primary key (pk).
        It then serializes the instance using the serializer defined for the view and
        returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Single Video Gallery instance
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        This method creates a new instance of the VideoGallery model using validated serializer data
        If the data is valid, it creates a new instance and
        returns a success response with a status code of 201.
        If the data is invalid, it returns an error response with a status code of 400.
        :return: response object
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['VIDEO_GALLERY']['CREATED_SUCCESSFULLY'],
                             'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        This method creates a new instance of the VideoGallery model using validated serializer data
        and the primary key of the instance to be updated.
        If the update is successful,it updates an existing instance and
        returns a success response with a status code of 201.
        If the update is unsuccessful it returns an error response with a status code of 400.
        :return: response object
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            response_data = {'message': SUCCESS_MESSAGES['VIDEO_GALLERY']['UPDATED_SUCCESSFULLY'],
                             'data': serializer.data}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        This method deletes an instance of the VideoGallery model using the primary key
        It also deletes the associated Video folder if it exists.
        It returns a success response with a message after the deletion is complete.
        :return: success response
        """
        instance = self.get_object()
        user = request.user
        username = user.get_username()
        folder_path = VIDEO_GALLERY_PATH.format(
            username=username, gallery_name=instance.gallery_name
        )
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        instance.delete()
        return Response({'message': SUCCESS_MESSAGES['VIDEO_GALLERY']['DELETED_SUCCESSFULLY']})


class VideoViewSet(viewsets.ModelViewSet):
    """
    The VideoViewSet handles Create and Delete operations for the VideoGallery model,
    with authentication required for all actions.
    It provides a serializer class for each action and
    filters queryset based on the authenticated user.
    """
    queryset = Video
    http_method_names = ['get', 'post', 'delete']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        """
        The get_serializer_class returns a serializer class based on the action being performed.
        For 'create' action, it returns VideoCreateSerializer,
        and for all other actions, it returns the default serializer, VideoSerializer.
        :return:serializer class
        """
        if self.action == 'create':
            return VideoCreateSerializer
        return VideoSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Image Model objects
        filtered based on the authenticated user.
        It orders the queryset based on the ID of the objects.
        :return: Image Gallery objects
        """
        user = self.request.user
        return Video.objects.filter(video_gallery__user=user).order_by('id')

    def list(self, request, *args, **kwargs):
        """
        The list retrieves all instances of the Video model.
        serializes them using the serializer returned by the get_serializer() method,
        and returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Video instances
        """
        queryset = self.get_queryset()
        videos = []
        for video in queryset:
            serializer = self.get_serializer(video)
            videos.append(serializer.data)
        return Response(videos, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        This method retrieves a single instance of the Video model
        using the provided primary key (pk).
        It then serializes the instance using the serializer defined for the view and
        returns the serialized data in a Response object with a status code of 200 (OK).
        :return: Single Video instance
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        This method creates a new instance of the Video model
        If the data is valid, it creates a new instance and
        returns a success response with a status code of 201.
        If the data is invalid, it returns an error response with a status code of 400.
        :return: response object
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            videos = serializer.create(serializer.validated_data)
            response_data = []
            for video in videos:
                video_url = request.build_absolute_uri(video.video.url)
                response_data.append({
                    'id': video.id,
                    'video': video_url,
                    'video_gallery_id': video.video_gallery_id,
                    'gallery': video.video_gallery.gallery_name,
                    'created_at': video.created_at,
                    'updated_at': video.updated_at,
                })
            return Response(
                {'message': SUCCESS_MESSAGES['VIDEO']['CREATED_SUCCESSFULLY'], 'data': response_data
                 },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        This method deletes an instance of the Video model using the primary key
        It also deletes the associated video folder if it exists.
        It returns a success response with a message after the deletion is complete.
        :return: success response
        """
        instance = self.get_object()
        video_path = VIDEO_PATH_TEMPLATE.format(MEDIA_URL, instance.video.name)
        os.remove(video_path)
        instance.delete()
        return Response({'message': SUCCESS_MESSAGES['VIDEO']['DELETED_SUCCESSFULLY']})
