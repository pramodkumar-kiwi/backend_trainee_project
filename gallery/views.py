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
from .constants import folder_name, media_name, gallery_field_name
from .messages import SUCCESS_MESSAGES
from .models import ImageGallery, VideoGallery, Image, Video
from .serializers import ImageGallerySerializer, ImageGalleryCreateSerializer, \
    ImageGalleryUpdateSerializer, VideoGallerySerializer, \
    VideoGalleryCreateSerializer, VideoGalleryUpdateSerializer, \
    ImageSerializer, ImageCreateSerializer, VideoSerializer, VideoCreateSerializer


class BaseGalleryViewSet(viewsets.ModelViewSet):
    """
    class BaseGalleryViewSet handles CRUD operations for
    'ImageGalleryViewSet' and 'VideoGalleryViewSet'
    """
    queryset = None
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']
    folder_name = None

    def get_queryset(self):
        """
         Get the queryset of current Gallery
        """
        user = self.request.user.id
        return self.queryset.objects.filter(user=user).order_by('id')

    def list(self, request, *args, **kwargs):
        """
        list all data for current Gallery
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        retrieves an instance of current Gallery
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        create new instance for current Gallery
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['BASE_GALLERY']['CREATED_SUCCESSFULLY'],
                             'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates the instance of Gallery with its new values
        """
        gal = self.get_object()
        serializer = self.get_serializer(gal, data=request.data)
        if serializer.is_valid():
            serializer.update(gal, serializer.validated_data)
            return Response({'message': SUCCESS_MESSAGES['BASE_GALLERY']['UPDATED_SUCCESSFULLY'],
                             'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
         Delete an instance of Gallery
        """
        instance = self.get_object()
        user = request.user.id
        folder_path = f"media/{user.username}/{self.folder_name}/{instance.gallery_name}"
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        instance.delete()
        return Response({'message': SUCCESS_MESSAGES['BASE_GALLERY']['DELETED_SUCCESSFULLY']})


class ImageGalleryViewSet(BaseGalleryViewSet):
    """
    class ImageGalleryViewSet for handling CRUD for ImageGallery
    """
    queryset = ImageGallery
    serializer_class = ImageGallerySerializer
    create_serializer_class = ImageGalleryCreateSerializer
    update_serializer_class = ImageGalleryUpdateSerializer
    folder_name = folder_name['IMAGE_folder_name']

    def get_serializer_class(self):
        """
        Get the Serializer Class as ImageGalleryCreateSerializer or ImageGalleryUpdateSerializer or
        ImageGallerySerializer as per required action
        """
        if self.action == 'create':
            return self.create_serializer_class
        if self.action == 'update':
            return self.update_serializer_class
        return self.serializer_class


class VideoGalleryViewSet(BaseGalleryViewSet):
    """
    class VideoGalleryViewSet for handling CRUD for VideoGallery
    """
    queryset = VideoGallery
    serializer_class = VideoGallerySerializer
    create_serializer_class = VideoGalleryCreateSerializer
    update_serializer_class = VideoGalleryUpdateSerializer
    folder_name = folder_name['VIDEO_folder_name']

    def get_serializer_class(self):
        """
        Get the Serializer Class as VideoGalleryCreateSerializer or VideoGalleryUpdateSerializer or
        VideoGallerySerializer as per required action
        """
        if self.action == 'create':
            return self.create_serializer_class
        if self.action == 'update':
            return self.update_serializer_class
        return self.serializer_class


class BaseMediaViewSet(viewsets.ModelViewSet):
    """
    class BaseMediaViewSet for Create,Read and Delete
    operations for 'ImageViewSet' and 'VideoViewSet'
    """
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]
    create_serializer_class = None
    serializer_class = None
    media_name = None
    gallery_field_name = None
    create_success_message = None
    delete_success_message = None

    def get_serializer_class(self):
        """
        Get the Serializer Class as create_serializer_class
        or serializer_class as per required action
        """
        if self.action == 'create':
            return self.create_serializer_class
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        list all data for current media
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        retrieves an instance of current media
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        create new instance for current media
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            media = serializer.create(serializer.validated_data)
            media_url = f"media/{getattr(media, self.media_name).name}"
            return Response({'message': self.create_success_message.format(media=self.media_name),
                             'data': {'media': media_url,
                                      f'{self.gallery_field_name}_id': getattr(media, self.gallery_field_name).id}},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an instance of current media
        """
        instance = self.get_object()
        media_path = f"media/{getattr(instance, self.media_name).name}"
        os.remove(media_path)
        instance.delete()
        return Response({'message': self.delete_success_message.format(media=self.media_name)})


class ImageViewSet(BaseMediaViewSet):
    """
    class ImageViewSet for Create,Read and Delete operations for 'ImageViewSet'
    """
    queryset = Image
    serializer_class = ImageSerializer
    create_serializer_class = ImageCreateSerializer
    media_name = media_name['IMAGE_media']
    gallery_field_name = gallery_field_name['Image_gallery_field']
    create_success_message = SUCCESS_MESSAGES["IMAGE"]["CREATED_SUCCESSFULLY"]
    delete_success_message = SUCCESS_MESSAGES["IMAGE"]["DELETED_SUCCESSFULLY"]

    def get_queryset(self):
        """
         Get the queryset of Image Model
        """
        user = self.request.user.id
        return self.queryset.objects.filter(image_gallery__user=user).order_by('id')


class VideoViewSet(BaseMediaViewSet):
    """
    class ImageViewSet for Create,Read and Delete operations for 'VideoViewSet'
    """
    queryset = Video
    serializer_class = VideoSerializer
    create_serializer_class = VideoCreateSerializer
    media_name = media_name['VIDEO_media']
    gallery_field_name = gallery_field_name['Video_gallery_field']
    create_success_message = SUCCESS_MESSAGES["VIDEO"]["CREATED_SUCCESSFULLY"]
    delete_success_message = SUCCESS_MESSAGES["VIDEO"]["DELETED_SUCCESSFULLY"]

    def get_queryset(self):
        """
         Get the queryset of Video Model
        """
        user = self.request.user.id
        return self.queryset.objects.filter(video_gallery__user=user).order_by('id')
