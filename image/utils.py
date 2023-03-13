"""
This file contains functions for generating unique filenames
and upload paths for images in the Image app.
"""
import os

from django.utils import timezone
from django.utils.text import slugify
from image.constants import FILENAME_FORMAT, IMAGE_UPLOAD_PATH


def generate_unique_filename(user, image_gallery, validated_data):
    """
    Function to generate a unique name to an image .
    The unique name that is generated has a name that includes
    username, gallery name, unique image number, date & time of image upload
    :param user: The User object representing the user who is uploading the image.
    :param image_gallery:The ImageGallery object representing the gallery where
    the image is being uploaded.
    :param validated_data: The validated data from the serializer,
    which should contain the image object being uploaded.
    :return: return a unique file or image name
    """
    current_time = timezone.now()
    image_count = image_gallery.image_gallery_set.count() + 1
    image_count_str = f"{image_count:02d}"
    filename, extension = os.path.splitext(validated_data['image'].name)
    slugify(filename)
    unique_filename = FILENAME_FORMAT.format(
        username=user.username,
        gallery_name=image_gallery.gallery_name,
        image_count_str=image_count_str,
        day=current_time.day,
        month=current_time.month,
        year=current_time.year,
        hour=current_time.hour,
        minute=current_time.minute,
        second=current_time.second,
        microsecond=current_time.microsecond,
        extension=extension
    )
    return unique_filename


def image_upload_path(instance, filename):
    """
    Generate Unique path for each image or file upload
    :param instance: instance of the model object being saved
    :param filename: name of the uploaded file
    :return: a unique path for the uploaded image file
    """
    return IMAGE_UPLOAD_PATH.format(
        username=instance.image_gallery.user.username,
        gallery_name=instance.image_gallery.gallery_name,
        filename=filename
    )
