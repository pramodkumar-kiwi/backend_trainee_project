"""
This module defines two Django serializers, `ImageGallerySerializer`&`ImageSerializer`
representing galleries and images respectively.
All serializers are associated with their respective models specified in their `Meta` classes.
"""
import os

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .constants import MAX_LENGTH, MIN_LENGTH
from .messages import VALIDATION
from .models import ImageGallery, Image


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer Image list images.
    """
    image = serializers.ImageField(required=True, error_messages=VALIDATION['image'])

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = Image
        fields = ['id', 'image']


class ImageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer ImageGallery creates a new gallery.
    """
    image = serializers.ImageField(required=True, error_messages=VALIDATION['image'])
    image_gallery_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['image_gallery_id'])

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Image instance
        """
        print(validated_data)
        user = self.context['request'].user

        image_gallery_id = validated_data.get('image_gallery_id')
        if not image_gallery_id:
            raise serializers.ValidationError(VALIDATION['image_gallery_id']['required'])

        image_data = validated_data.get('image')
        if not image_data:
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


class ImageGallerySerializer(serializers.ModelSerializer):
    """
     Serializer ImageGallery list a gallery.
     """
    image_gallery_set = ImageSerializer(many=True, read_only=True)
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
        required=True, error_messages=VALIDATION['gallery_name'])

    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the serializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name', 'image_gallery_set']


class ImageGalleryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer ImageGallery creates a new gallery.
    """
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
        required=True, error_messages=VALIDATION['gallery_name'])

    @staticmethod
    def validate_image_gallery_set(value):
        """
        Validate that each gallery has no more than 10 images.
        :param value:image_gallery_set
        :return:if valid return value ,else return Validation error
        """
        if len(value) > 10:
            raise serializers.ValidationError(VALIDATION['image_gallery_set']['max_limit'])
        return value

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
    Serializer ImageGalleryCreate updates
    an existing Image Gallery .
    """
    gallery_name = serializers.CharField(min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
                                         required=True, error_messages=VALIDATION['gallery_name'])

    @staticmethod
    def validate_image_gallery_set(value):
        """
        Validate that each gallery has no more than 10 images.
        :param value:image_gallery_set
        :return:if valid return value ,else return Validation error
        """
        if len(value) > 10:
            raise serializers.ValidationError(VALIDATION['image_gallery_set']['max_limit'])
        return value

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
