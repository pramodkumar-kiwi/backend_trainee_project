"""
Admin panel for ImageGallery,Image,VideoGallery and Video
"""

from django.contrib import admin
from gallery.models import Video, VideoGallery


@admin.register(VideoGallery)
class VideoGalleryAdmin(admin.ModelAdmin):
    """
    Class VideoGalleryAdmin display all the fields of VideoGallery model in admin panel
    """
    list_display = ('id', 'gallery_name', 'created_at', 'updated_at')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Class VideoAdmin display all the fields of Videos in admin panel
    """
    list_display = ('id', 'video', 'created_at', 'updated_at')
