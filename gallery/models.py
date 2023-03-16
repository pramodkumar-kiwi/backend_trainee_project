"""
This module defines Django models `ImageGallery`,'VideoGallery','Image' and 'Video'.
"""
from django.db import models
from account.models import User
from .utils import video_upload_path


class VideoGallery(models.Model):
    """
    The VideoGallery model with gallery name and foreign key to User model
    representing the user who owns the gallery.
    """
    gallery_name = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_gallery_user_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.gallery_name)

    class Meta:
        """
       class Meta to specify the database table
        for VideoGallery model
        """
        db_table = 'VideoGallery'


class Video(models.Model):
    """
    The Video model with video name and foreign key to VideoGallery model
    representing the gallery in which video is uploaded.
    """

    video_gallery = models.ForeignKey(
        VideoGallery,
        on_delete=models.CASCADE,
        related_name='video_gallery_set')
    video = models.FileField(upload_to=video_upload_path, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.video)

    class Meta:
        """
        Use the Meta class to specify the database table
        for Video model
        """
        db_table = 'Video'
