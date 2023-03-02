"""
This module defines two Django admin `VideoGalleryAdmin` and 'VideoAdmin' representing
VideoGallery and Video.
These are associated with their respective models ImageGallery and Image.
"""
from django.contrib import admin
from video.models import VideoGallery, Video


@admin.register(VideoGallery)
class VideoGalleryAdmin(admin.ModelAdmin):
    """
    Class VideoGalleryAdmin display all the fields of VideoGallery model in admin panel
    """
    list_display = ('id', 'name', 'created_at', 'updated_at')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Class VideoAdmin display all the fields of Video model in admin panel
    """
    list_display = ('id', 'video', 'created_at', 'updated_at')
