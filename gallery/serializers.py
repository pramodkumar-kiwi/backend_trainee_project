"""
This module defines different Django serializers,
representing image-gallery, images ,video-gallery and videos.
All serializers are associated with their respective models specified in their `Meta` classes.
"""
import os
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .constants import MAX_LENGTH, MIN_LENGTH, VIDEO_GALLERY_PATH, MAX_LIMIT, MAX_SIZE, VIDEO_FORMAT
from .messages import VALIDATION
from .models import VideoGallery, Video
from .utils import generate_unique_video_filename


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer VideoSerializer to list videos.
    """
    video = serializers.SerializerMethodField()
    video_gallery_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['video_gallery_id'])
    gallery_name = serializers.SerializerMethodField()

    def get_video(self, obj):
        """
        Returns the absolute URL of a video associated with the given object.
        :param obj:Video object
        :return: The absolute URL of the video
        """
        if obj.video:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.video.url)
        return None

    @staticmethod
    def get_gallery_name(obj):
        """
        Serializer method to return the gallery name
        of the related VideoGallery instance.
        """
        return obj.video_gallery.gallery_name

    class Meta:
        """
        class Meta to specify the model and fields
        that the serializer should work with
        """
        model = Video
        fields = ['id', 'video', 'video_gallery_id', 'gallery_name']


class VideoGallerySerializer(serializers.ModelSerializer):
    """
     Serializer VideoGallerySerializer list a video gallery.
     """
    video_gallery_set = VideoSerializer(many=True, read_only=True)
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['video_gallery_name'], max_length=MAX_LENGTH['video_gallery_name'],
        required=True, error_messages=VALIDATION['video_gallery_name'])

    class Meta:
        """
        class Meta to specify the model and fields
        that the serializer should work with
        """
        model = VideoGallery
        fields = ['id', 'gallery_name', 'video_gallery_set']


class VideoGalleryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer VideoGalleryCreateSerializer creates a new video gallery.
    """
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['video_gallery_name'], max_length=MAX_LENGTH['video_gallery_name'],
        required=True, error_messages=VALIDATION['video_gallery_name'])

    @staticmethod
    def validate_gallery_name(value):
        """
        Validator function to check if a video gallery with the given name already exists
        """
        if VideoGallery.objects.filter(gallery_name=value).exists():
            raise serializers.ValidationError(VALIDATION['video_gallery_name']['exists'])
        return value

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new VideoGallery instance
        """
        user = self.context['request'].user
        video_gallery = VideoGallery.objects.create(user=user, **validated_data)
        path = VIDEO_GALLERY_PATH.format(
            username=user.username, gallery_name=video_gallery.gallery_name
        )
        os.makedirs(path, exist_ok=False)
        return video_gallery

    class Meta:
        """
        class Meta to specify the model and fields
        that the serializer should work with
        """
        model = VideoGallery
        fields = ['id', 'gallery_name']


class VideoGalleryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer VideoGalleryUpdateSerializer
    updates an existing Video Gallery .
    """
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['video_gallery_name'],
        max_length=MAX_LENGTH['video_gallery_name'],
        required=True,
        error_messages=VALIDATION['video_gallery_name'])

    def validate_gallery_name(self, value):
        """
               Validation to check if gallery already exists
               :param value: gallery_name
               :return: if valid return value, else return Validation error
               """
        user = self.context['request'].user
        if VideoGallery.objects.filter(user=user, gallery_name=value).exists():
            raise serializers.ValidationError(VALIDATION['VALIDATION']['exists_while_updating'])
        return value

    def update(self, instance, validated_data):
        """
        Override the update method to add custom behavior
        when updating an existing VideoGallery instance
        """
        user = self.context['request'].user
        VideoGallery.objects.filter(id=instance.id).update(**validated_data)
        old_path = VIDEO_GALLERY_PATH.format(
            username=user.username, gallery_name=instance.gallery_name
        )
        new_path = VIDEO_GALLERY_PATH.format(
            username=user.username, gallery_name=validated_data['gallery_name']
        )
        os.rename(old_path, new_path)
        updated_instance = VideoGallery.objects.get(id=instance.id)
        return updated_instance

    class Meta:
        """
        class Meta to specify the model and fields
        that the serializer should work with
        """
        model = VideoGallery
        fields = ['id', 'gallery_name']


class VideoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model creating a new Video instance with two required fields:
    'gallery' and 'video_gallery_id'.
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    video = serializers.ListField(
        child=serializers.FileField(),
        required=True,
        error_messages=VALIDATION['video']
    )
    video_gallery_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['video_gallery_id'])

    @staticmethod
    def validate_video(value):
        """
        Custom validation function to ensure that the video file format is mp4
        and the size of each file is less than 50MB
        """
        for file in value:
            filename, ext = os.path.splitext(file.name)
            if ext.lower() != VIDEO_FORMAT:
                raise serializers.ValidationError(VALIDATION['video']['format'])
            if file.size > MAX_SIZE['max_size']:
                raise serializers.ValidationError(VALIDATION['video']['max_size'])
        return value

    def validate(self, attrs):
        """
        Validation to check user cannot
        upload more than 10 videos in a single gallery
        :param attrs: video_gallery_id
        :return: if valid return attrs ,else return Validation error
        """
        video_gallery_id = attrs.get('video_gallery_id')
        user = self.context['request'].user
        if video_gallery_id:
            gallery = get_object_or_404(VideoGallery, id=video_gallery_id, user=user)
            videos = attrs.get('video', [])
            if len(videos) + gallery.video_gallery_set.count() > MAX_LIMIT['max_limit']:
                raise serializers.ValidationError(VALIDATION['video_gallery_set']['max_limit'])
        return attrs

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Image instance
        It generates a unique filename for the uploaded image
        """
        user = self.context['request'].user
        video_gallery = get_object_or_404(
            VideoGallery, id=validated_data['video_gallery_id'], user=user
        )
        videos = []
        for video in validated_data['video']:
            video_name = generate_unique_video_filename(user, video_gallery, validated_data)
            video.name = str(video_name)
            video_instance = Video(
                video_gallery=video_gallery,
                video=video,
            )
            videos.append(video_instance)
        Video.objects.bulk_create(videos)
        return videos

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the VideoCreateSerializer should work with
        """
        model = Video
        fields = ['id', 'video', 'video_gallery_id']
