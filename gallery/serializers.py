"""
This file contains different serializers for Image and ImageGallery objects.
They handle serialization and deserialization of these objects,
and also include validation and creation/update logic.
The ImageCreateSerializer checks for gallery size and user limits, and creates a unique filename.
The ImageGalleryCreateSerializer creates a new directory for the gallery's images,
while the ImageGalleryUpdateSerializer renames the directory if the gallery name is updated.
"""
import os

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from gallery.constants import MAX_LENGTH, MIN_LENGTH, IMAGE_GALLERY_PATH, MAX_LIMIT, \
    MAX_SIZE_IMAGE, IMAGE_GALLERY
from gallery.messages import VALIDATION
from gallery.models import ImageGallery, Image
from gallery.utils import generate_unique_image


class ImageSerializer(serializers.ModelSerializer):
    """
     Serializer for the Image model with two required fields:
     'gallery' and 'image_gallery_id'.
     The 'error_messages' argument is used to specify custom error messages
     in case of validation errors.
    """
    image = serializers.SerializerMethodField()
    image_gallery_id = serializers.IntegerField(
        required=True, error_messages=VALIDATION['image_gallery_id'])

    def get_image(self, obj):
        """
        Returns the absolute URL of an image associated with the given object.
        :param obj:Image object
        :return: The absolute URL of the image
        """
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        return None

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the ImageSerializer should work with
        """
        model = Image
        fields = ['id', 'image', 'image_gallery_id', 'created_at', 'updated_at']


class ImageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Image model creating a new Image instance with two required fields:
    'gallery' and 'image_gallery_id'.
    The 'error_messages' argument is used to specify custom error messages
    in case of validation errors.
    """
    image = serializers.ListField(
        child=serializers.ImageField(),
        required=True,
        error_messages=VALIDATION['image']
    )
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
            images = attrs.get('image', [])
            if len(images) + gallery.image_gallery_set.count() > MAX_LIMIT['max_limit']:
                raise serializers.ValidationError(VALIDATION['image_gallery_set']['max_limit'])
        return attrs

    @staticmethod
    def validate_image(value):
        """
        This function validates the size of the uploaded gallery and
        raises a validation error if it exceeds the maximum size limit specified in MAX_SIZE
        :param value: gallery
        :return: if valid return value ,else return Validation error
        """
        for image in value:
            if image.size > MAX_SIZE_IMAGE['max_size']:
                raise serializers.ValidationError(VALIDATION['image']['max_size'])
            return value

    def create(self, validated_data):
        """
        Override the create method to add custom behavior
        when creating a new Image instance
        It generates a unique filename for the uploaded image
        """
        user = self.context['request'].user
        image_gallery = get_object_or_404(
            ImageGallery, id=validated_data['image_gallery_id'], user=user
        )
        images = []

        for image in validated_data['image']:
            image_name = generate_unique_image(user, image_gallery, validated_data)
            image.name = str(image_name)
            image_instance = Image(
                image_gallery=image_gallery,
                image=image,
            )
            images.append(image_instance)
        Image.objects.bulk_create(images)
        return images

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the ImageCreateSerializer should work with
        """
        model = Image
        fields = ['id', 'image', 'image_gallery_id', 'created_at', 'updated_at']


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
        fields = ['id', 'gallery_name', 'image_gallery_set', 'created_at', 'updated_at']


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
        It then generates a path for the new gallery using a string format method,
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
        fields = ['id', 'gallery_name', 'created_at', 'updated_at']


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
        The method then generates old and new paths for the gallery using a
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
        # get all the images in the gallery being updated
        images = Image.objects.filter(image_gallery=instance)
        # update the paths of all the images with the new gallery name
        for image in images:
            image_path = os.path.join(
                IMAGE_GALLERY.format(
                    username=user.username, gallery_name=validated_data['gallery_name']
                ),
                image.image.name.split('/')[-1]
            )
            image.image.name = image_path
            Image.objects.bulk_update(images, ['image'])

        updated_instance = ImageGallery.objects.get(id=instance.id)

        return updated_instance

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the model and fields
        that the ImageGalleryUpdateSerializer should work with
        """
        model = ImageGallery
        fields = ['id', 'gallery_name', 'created_at', 'updated_at']
