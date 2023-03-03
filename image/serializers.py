"""
This module defines two Django serializers, `ImageGallerySerializer`&`ImageSerializer`
representing galleries and images respectively.
All serializers are associated with their respective models specified in their `Meta` classes.
"""
import os
from rest_framework import serializers
from account.serializers import SignupSerializer
from .models import ImageGallery


class ImageGallerySerializer(serializers.ModelSerializer):
    """
     Serializer ImageGallery list a gallery.
     """
    user = SignupSerializer(read_only=True)
    gallery_name = serializers.CharField(min_length=5, max_length=20, required=True)

    class Meta:
        """
        Use the Meta class to specify the model and fields that the serializer should work with
        """
        model = ImageGallery
        fields = ['id', 'user', 'gallery_name']


class ImageGalleryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer ImageGallery creates a new gallery.
    """
    gallery_name = serializers.CharField(min_length=5, max_length=20, required=True)

    def create(self, validated_data):
        user = self.context['request'].user
        image_gallery = ImageGallery.objects.create(**validated_data)
        os.makedirs(f'media/{user.username}/{image_gallery.gallery_name}')
        return image_gallery

    class Meta:
        """
        Use the Meta class to specify the model and fields that the serializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name']


class ImageGalleryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer ImageGalleryCreate updates an existing Image Gallery .
    """
    gallery_name = serializers.CharField(min_length=5, max_length=20, required=True)

    def update(self, instance, validated_data):
        """
        Override the update method to add custom behavior
        when updating an existing ImageGallery instance
        """
        return ImageGallery.objects.filter(id=instance.id).update(**validated_data)

    class Meta:
        """
        Use the Meta class to specify the model and fields that the serializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name']
