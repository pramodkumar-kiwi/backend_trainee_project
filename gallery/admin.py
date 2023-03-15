"""
This file defines two Django admin `ImageGalleryAdmin` and 'ImageAdmin' representing
ImageGallery and Image.
These are associated with their respective models ImageGallery and Image.
"""
from django.contrib import admin
from gallery.models import ImageGallery, Image


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    """
    Class ImageGalleryAdmin display all the fields of ImageGallery model in admin panel
    """
    list_display = ('id', 'gallery_name', 'created_at', 'updated_at')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Class ImageGalleryAdmin display all the fields of ImageGallery model in admin panel
    """
    list_display = ('id', 'image', 'created_at', 'updated_at')
