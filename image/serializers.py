"""
This file contains different serializers for Image and ImageGallery objects.
They handle serialization and deserialization of these objects,
and also include validation and creation/update logic.
The ImageCreateSerializer checks for image size and user limits, and creates a unique filename.
The ImageGalleryCreateSerializer creates a new directory for the gallery's images,
while the ImageGalleryUpdateSerializer renames the directory if the gallery name is updated.
"""
import os
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from image.constants import MAX_LENGTH, MIN_LENGTH, IMAGE_GALLERY_PATH, MAX_LIMIT, MAX_SIZE
from image.messages import VALIDATION
from image.models import ImageGallery, Image
from image.utils import generate_unique_filename


class ImageSerializer(serializers.ModelSerializer):
    """
     Serializer for the Image model with two required fields:
     'image' and 'image_gallery_id'.
     The 'error_messages' argument is used to specify custom error messages
     in case of validation errors.
    """
    image = serializers.ImageField(required=True, error_messages=VALIDATION['image'])
    image_gallery_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['image_gallery_id'])

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the ImageSerializer should work with
        """
        model = Image
        fields = ['id', 'image', 'image_gallery_id']


class ImageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Image model creating a new Image instance with two required fields:
    'image' and 'image_gallery_id'.
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    image = serializers.ImageField(required=True, error_messages=VALIDATION['image'])
    image_gallery_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['image_gallery_id'])

    def validate(self, attrs):
        """
        Validation to check user cannot
        upload more than 10 images in a single gallery
        :param attrs: image_gallery_id
        :return: if valid return attrs ,else return Validation error
        """
        image_gallery_id = attrs.get('image_gallery_id')
        user = self.context['request'].user
        if image_gallery_id:
            gallery = get_object_or_404(ImageGallery, id=image_gallery_id, user=user)
            if gallery.image_gallery_set.count() >= MAX_LIMIT['max_limit']:
                raise serializers.ValidationError(VALIDATION['image_gallery_set']['max_limit'])
        return attrs

    @staticmethod
    def validate_image(value):
        """
        This function validates the size of the uploaded image and
        raises a validation error if it exceeds the maximum size limit specified in MAX_SIZE
        :param value: image
        :return: if valid return value ,else return Validation error
        """
        if value.size > MAX_SIZE['max_size']:
            raise serializers.ValidationError(VALIDATION['image']['max_size'])
        return value

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Image instance
        It generates a unique filename for the uploaded image and sets the name of the image
        """
        user = self.context['request'].user
        image_gallery = get_object_or_404(
            ImageGallery, id=validated_data['image_gallery_id'], user=user
        )
        validated_data['image'].name = generate_unique_filename(user, image_gallery, validated_data)
        return Image.objects.create(image_gallery=image_gallery, **validated_data)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the ImageCreateSerializer should work with
        """
        model = Image
        fields = ['id', 'image', 'image_gallery_id']


class ImageGallerySerializer(serializers.ModelSerializer):
    """
    Serializer for the ImageGallery model with two required fields:
    'image_gallery_set' and 'gallery_name'.
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    image_gallery_set = ImageSerializer(many=True, read_only=True)
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
        required=True, error_messages=VALIDATION['gallery_name'])

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the ImageGallerySerializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name', 'image_gallery_set']


class ImageGalleryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the ImageGallery model creating a new ImageGallery instance with
    one required field:'gallery_name'.
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    gallery_name = serializers.CharField(
        min_length=MIN_LENGTH['gallery_name'], max_length=MAX_LENGTH['gallery_name'],
        required=True, error_messages=VALIDATION['gallery_name'])

    def validate_gallery_name(self, value):
        """
        Validation to check if gallery already exists
        :param value: gallery_name
        :return: if valid return value, else return Validation error
        """
        user = self.context['request'].user
        if ImageGallery.objects.filter(user=user, gallery_name=value).exists():
            raise serializers.ValidationError(VALIDATION['gallery_name']['exists'])

        return value

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new ImageGallery instance
        It then generates a path for the new image gallery using a string format method,
        and creates the directory specified in the path using
        'os.makedirs' with the 'exist_ok' parameter set to True.
        """
        user = self.context['request'].user
        image_gallery = ImageGallery.objects.create(user=user, **validated_data)
        path = IMAGE_GALLERY_PATH.format(
            username=user.username, gallery_name=image_gallery.gallery_name
        )
        os.makedirs(path, exist_ok=False)
        return image_gallery

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the ImageGalleryCreateSerializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name']


class ImageGalleryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the ImageGallery model updating an existing ImageGallery instance
    with one required field: 'gallery_name'.
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    gallery_name = serializers.CharField(min_length=MIN_LENGTH['gallery_name'],
                                         max_length=MAX_LENGTH['gallery_name'],
                                         required=True, error_messages=VALIDATION['gallery_name'])

    def validate_gallery_name(self, value):
        """
        Validation to check if gallery already exists
        :param value: gallery_name
        :return: if valid return value, else return Validation error
        """
        user = self.context['request'].user
        if ImageGallery.objects.filter(user=user, gallery_name=value).exists():
            raise serializers.ValidationError(VALIDATION['gallery_name']['exists'])

        return value

    def update(self, instance, validated_data):
        """
        Override the update method to add custom behavior
        when updating an existing ImageGallery instance
        The method then generates old and new paths for the image gallery using a
        string format method,and renames the old directory to the new directory using 'os.rename'.
        """
        user = self.context['request'].user
        ImageGallery.objects.filter(id=instance.id).update(**validated_data)
        old_path = IMAGE_GALLERY_PATH.format(
            username=user.username, gallery_name=instance.gallery_name
        )
        new_path = IMAGE_GALLERY_PATH.format(
            username=user.username, gallery_name=validated_data['gallery_name']
        )
        os.rename(old_path, new_path)
        updated_instance = ImageGallery.objects.get(id=instance.id)
        return updated_instance

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the ImageUpdateSerializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name']
