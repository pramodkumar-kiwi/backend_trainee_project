"""
This file contains functions for generating unique filenames
and upload paths for images in the Image app.
"""
import os

from django.utils import timezone
from django.utils.text import slugify
from gallery.constants import IMAGE_UPLOAD_PATH, VIDEO_UPLOAD_PATH, IMAGE_FILENAME_FORMAT, VIDEO_FILENAME_FORMAT


def generate_unique_image_filename(user, image_gallery, validated_data):
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
    unique_filename = IMAGE_FILENAME_FORMAT.format(
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


def generate_unique_video_filename(user, video_gallery, validated_data):
    """
    Function to generate a unique name to a video .
    The unique name that is generated has a name that includes
    username, gallery name, unique video number, date & time of video upload
    :param user: The User object representing the user who is uploading the video.
    :param video_gallery:The VideoGallery object representing the gallery where
    the video is being uploaded.
    :param validated_data: The validated data from the serializer,
    which should contain the video object being uploaded.
    :return: return a unique file or video name
    """
    current_time = timezone.now()
    video_count = video_gallery.video_gallery_set.count() + 1
    video_count_str = f"{video_count:02d}"
    filename, extension = os.path.splitext(validated_data['video'].name)
    slugify(filename)
    unique_filename = VIDEO_FILENAME_FORMAT.format(
        username=user.username,
        gallery_name=video_gallery.gallery_name,
        video_count_str=video_count_str,
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
    Gives path to the uploaded images.
    """
    return IMAGE_UPLOAD_PATH.format(
        username=instance.image_gallery.user.username,
        gallery_name=instance.image_gallery.gallery_name,
        filename=filename
    )


def video_upload_path(instance, filename):
    """
        Gives path to the uploaded videos.
        """
    return VIDEO_UPLOAD_PATH.format(
        username=instance.video_gallery.user.username,
        gallery_name=instance.video_gallery.gallery_name,
        filename=filename
    )
