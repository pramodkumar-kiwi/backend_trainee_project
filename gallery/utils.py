"""
This file contains functions for generating unique filenames
and upload paths for images in the Image app.
"""
import os

from django.utils import timezone
from django.utils.text import slugify
from gallery.constants import FILENAME_FORMAT, IMAGE_UPLOAD_PATH


def generate_unique_image(user, image_gallery, validated_data):
    """
    Function to generate a unique name for each image in the list.
    The unique name that is generated has a name that includes
    username, gallery name, unique gallery number, date & time of gallery upload
    :param user: The User object representing the user who is uploading the gallery.
    :param image_gallery:The ImageGallery object representing the gallery where
    the gallery is being uploaded.
    :param validated_data: The validated data from the serializer,
    which should contain the list of images being uploaded.
    :return: return a list of unique file or gallery names
    """
    current_time = timezone.now()
    unique_filenames = []
    for image in validated_data['image']:
        filename, extension = os.path.splitext(image.name)
        slugify(filename)
        unique_filename = FILENAME_FORMAT.format(
            username=user.username,
            gallery_name=image_gallery.gallery_name,
            day=current_time.day,
            month=current_time.month,
            year=current_time.year,
            hour=current_time.hour,
            minute=current_time.minute,
            second=current_time.second,
            microsecond=current_time.microsecond,
            extension=extension
        )
        unique_filenames.append(unique_filename)
        print(unique_filenames)
    return unique_filenames


def image_upload_path(instance, filename):
    """
    Generate Unique path for each gallery or file upload
    :param instance: instance of the model object being saved
    :param filename: name of the uploaded file
    :return: a unique path for the uploaded gallery file
    """
    return IMAGE_UPLOAD_PATH.format(
        username=instance.image_gallery.user.username,
        gallery_name=instance.image_gallery.gallery_name,
        filename=filename
    )
