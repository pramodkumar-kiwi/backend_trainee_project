"""
This module defines Django models `VideoGallery` and 'Video' representing gallery and video .
These models are associated with their respective database tables specified in their `Meta` class.
"""
from django.db import models
from account.models import User


class VideoGallery(models.Model):
    """
    The VideoGallery model with gallery name and foreign key to User model
    representing the user who owns the gallery.
    """
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_gallery_user_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        """
        Use the Meta class to specify the database table
        for ImageGallery model
        """
        db_table = 'VideoGallery'


class Video(models.Model):
    """
    The Video model with video name and foreign key to VideoGallery model
    representing the gallery in which video is uploaded.
    """
    video_gallery = models.ForeignKey(VideoGallery, on_delete=models.CASCADE, related_name='video_gallery_set')
    video = models.FileField(upload_to='media/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.video

    class Meta:
        """
        Use the Meta class to specify the database table
        for Video model
        """
        db_table = 'Video'
