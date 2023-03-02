"""
This module defines two Django serializers, `ImageGallerySerializer`&`ImageSerializer`
representing galleries and images respectively.
All serializers are associated with their respective models specified in their `Meta` classes.
"""
from rest_framework import serializers
from .models import ImageGallery, Image


class ImageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Image upload a new image.
    """
    image = serializers.ImageField()

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Image instance
        """
        return Image.objects.create(**validated_data)

    class Meta:
        model = Image
        fields = ['id', 'image']


class ImageUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer Image upload a new image.
    """
    image = serializers.ImageField()

    def update(self, instance, validated_data):
        """
        Override the update method to add custom behavior
        when updating an existing ImageGallery instance
        """
        return Image.objects.filter(id=instance.id).update(**validated_data)

    class Meta:
        model = Image
        fields = ['id', 'image']


class ImageGalleryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer ImageGallery creates a new gallery.
    """
    image_gallery_set = ImageCreateSerializer(many=True, read_only=True)
    gallery_name = serializers.CharField(min_length=5, max_length=20, required=True)

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new ImageGallery instance
        """
        return ImageGallery.objects.create(**validated_data)

    class Meta:
        """
        Use the Meta class to specify the model and fields that the serializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name', 'image_gallery_set']


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