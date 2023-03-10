"""
This module defines two Django serializers,
representing galleries, images and videos.
All serializers are associated with their respective models specified in their `Meta` classes.
"""
import os
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .constants import MAX_LENGTH, MIN_LENGTH
from .messages import VALIDATION
from .models import ImageGallery, VideoGallery, Image, Video


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer ImageSerializer list images.
    """
    image = serializers.ImageField(required=True, error_messages=VALIDATION['image'])
    image_gallery_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['image_gallery_id'])

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = Image
        fields = ['id', 'image', 'image_gallery_id']


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer VideoSerializer list videos.
    """
    video = serializers.FileField(required=True, error_messages=VALIDATION['video'])

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = Video
        fields = ['id', 'video', 'video_gallery_id']


class ImageGallerySerializer(serializers.ModelSerializer):
    """
     Serializer ImageGallerySerializer list a image gallery.
     """
    image_gallery_set = ImageSerializer(many=True, read_only=True)
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
        required=True, error_messages=VALIDATION['image_gallery_name'])

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name', 'image_gallery_set']


class ImageGalleryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer ImageGalleryCreateSerializer creates a new image gallery.
    """
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
        required=True, error_messages=VALIDATION['image_gallery_name'])

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new ImageGallery instance
        """
        user = self.context['request'].user
        image_gallery = ImageGallery.objects.create(user=user, **validated_data)
        os.makedirs(f'media/{user.username}/image/{image_gallery.gallery_name}', exist_ok=True)
        return image_gallery

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name']


class ImageGalleryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer ImageGalleryUpdateSerializer updates
    an existing Image Gallery .
    """
    gallery_name = serializers.CharField(min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
                                         required=True, error_messages=VALIDATION['image_gallery_name'])

    def update(self, instance, validated_data):
        """
        Override the update method to add custom behavior
        when updating an existing ImageGallery instance
        """
        user = self.context['request'].user
        ImageGallery.objects.filter(id=instance.id).update(**validated_data)
        os.rename(f'media/{user.username}/image/{instance.gallery_name}',
                  f'media/{user.username}/image/{validated_data["gallery_name"]}')
        updated_instance = ImageGallery.objects.get(id=instance.id)
        return updated_instance

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name']


class VideoGallerySerializer(serializers.ModelSerializer):
    """
     Serializer VideoGallerySerializer list a video gallery.
     """
    video_gallery_set = VideoSerializer(many=True, read_only=True)
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
        required=True, error_messages=VALIDATION['video_gallery_name'])

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = VideoGallery
        fields = ['id', 'gallery_name', 'video_gallery_set']


class VideoGalleryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer VideoGalleryCreateSerializer creates a new video gallery.
    """
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
        required=True, error_messages=VALIDATION['video_gallery_name'])

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
        os.makedirs(f'media/{user.username}/video/{video_gallery.gallery_name}', exist_ok=True)
        return video_gallery

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = VideoGallery
        fields = ['id', 'gallery_name']


class VideoGalleryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer VideoGalleryUpdateSerializer updates
    an existing Video Gallery .
    """
    gallery_name = serializers.CharField(min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
                                         required=True, error_messages=VALIDATION['video_gallery_name'])

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
        os.rename(f'media/{user.username}/video/{instance.gallery_name}',
                  f'media/{user.username}/video/{validated_data["gallery_name"]}')
        updated_instance = VideoGallery.objects.get(id=instance.id)
        return updated_instance

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = VideoGallery
        fields = ['id', 'gallery_name']


class ImageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer ImageCreateSerializer creates a new image.
    """
    image = serializers.ImageField(required=True, error_messages=VALIDATION['image'])
    image_gallery_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['image_gallery_id'])

    def validate(self, attrs):
        """
        Validation to check user cannot
        upload more than 10 images in a single gallery
        :param attrs: image_gallery
        :return: if valid return value ,else return Validation error
        """
        image_gallery_id = attrs.get('image_gallery_id')
        user = self.context['request'].user
        if image_gallery_id:
            gallery = get_object_or_404(ImageGallery, id=image_gallery_id, user=user)
            if gallery.image_gallery_set.count() >= 10:
                raise serializers.ValidationError(VALIDATION['image_gallery_set']['max_limit'])
        return attrs

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Image instance
        """
        user = self.context['request'].user

        image_gallery_id = validated_data.get('image_gallery_id')
        if not image_gallery_id:
            raise serializers.ValidationError(VALIDATION['image_gallery_id']['required'])

        image = validated_data.get('image')
        if not image:
            raise serializers.ValidationError(VALIDATION['image_gallery_id']['required'])

        image_gallery = get_object_or_404(ImageGallery, id=image_gallery_id, user=user)
        image = Image.objects.create(image_gallery=image_gallery, **validated_data)
        return image

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = Image
        fields = ['id', 'image', 'image_gallery_id']


class VideoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer VideoCreateSerializer creates a new video.
    """
    video = serializers.FileField(required=True, error_messages=VALIDATION['image'])
    video_gallery_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['video_gallery_id'])

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Video instance
        """
        print(validated_data)
        user = self.context['request'].user

        video_gallery_id = validated_data.get('video_gallery_id')
        if not video_gallery_id:
            raise serializers.ValidationError(VALIDATION['video_gallery_id']['required'])

        video = validated_data.get('video')
        if not video:
            raise serializers.ValidationError(VALIDATION['video_gallery_id']['required'])

        video_gallery = get_object_or_404(VideoGallery, id=video_gallery_id, user=user)
        video = Video.objects.create(video_gallery=video_gallery, **validated_data)
        return video

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = Video
        fields = ['id', 'video', 'video_gallery_id']
