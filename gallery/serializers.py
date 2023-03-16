"""
This module defines different Django serializers,
representing image-gallery, images ,video-gallery and videos.
All serializers are associated with their respective models specified in their `Meta` classes.
"""
import os
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .constants import MAX_LENGTH, MIN_LENGTH, VIDEO_GALLERY_PATH
from .messages import VALIDATION
from .models import VideoGallery, Video
from .utils import generate_unique_video_filename


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer VideoSerializer to list videos.
    """
    video = serializers.FileField(required=True, error_messages=VALIDATION['video'])
    gallery_name = serializers.SerializerMethodField()

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

    @staticmethod
    def validate_video_gallery_set(value):
        """
        Validate that each gallery has no more than 10 videos.
        :param value:video_gallery_set
        :return:if valid return value ,else return Validation error
        """
        if len(value) > 10:
            raise serializers.ValidationError(VALIDATION['video_gallery_set']['max_limit'])
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
        Check if the gallery_name already exists for the current user.
        """
        user = self.context['request'].user
        gallery_name_exists = VideoGallery.objects.filter(
            user=user, gallery_name=value).exclude(
            id=self.instance.id).exists()
        if gallery_name_exists:
            raise serializers.ValidationError(
                VALIDATION['video_gallery_name']['exists_while_updating'])
        return value

    @staticmethod
    def validate_video_gallery_set(value):
        """
        Validate that each gallery has no more than 10 videos.
        :param value:video_gallery_set
        :return:if valid return value ,else return Validation error
        """
        if len(value) > 10:
            raise serializers.ValidationError(VALIDATION['video_gallery_set']['max_limit'])
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
    Serializer VideoCreateSerializer creates a new video.
    """
    video = serializers.FileField(required=True, error_messages=VALIDATION['video'])
    gallery_name = serializers.SerializerMethodField()
    video_gallery_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['video_gallery_id'])

    @staticmethod
    def get_gallery_name(obj):
        """
        Serializer method to return the gallery name
        of the related VideoGallery instance.
        """
        return obj.video_gallery.gallery_name

    def validate(self, attrs):
        """
        Validation to check user cannot
        upload more than 10 videos in a single gallery
        :param attrs: video_gallery
        :return: if valid return value ,else return Validation error
        """
        video_gallery_id = attrs.get('video_gallery_id')
        user = self.context['request'].user
        if video_gallery_id:
            gallery = get_object_or_404(VideoGallery, id=video_gallery_id, user=user)
            if gallery.video_gallery_set.count() >= 10:
                raise serializers.ValidationError(VALIDATION['video_gallery_set']['max_limit'])
        return attrs

    @staticmethod
    def validate_video(value):
        """
        validate a user to upload only video format file
        :param value: video
        :return: if valid return value ,else return Validation error
        """
        if not value.name.endswith('.mp4'):
            raise serializers.ValidationError(VALIDATION['video']['video-format'])

        return value

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Video instance
        It generates a unique filename for the uploaded
        Videos and sets the name of the Video
        """
        user = self.context['request'].user
        video_gallery = get_object_or_404(
            VideoGallery, id=validated_data['video_gallery_id'], user=user
        )
        validated_data['video'].name = generate_unique_video_filename(
            user, video_gallery, validated_data)
        return Video.objects.create(video_gallery=video_gallery, **validated_data)

    class Meta:
        """
        class Meta to specify the model and fields
        that the serializer should work with
        """
        model = Video
        fields = ['id', 'video', 'video_gallery_id', 'video', 'gallery_name']
