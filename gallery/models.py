"""
This file defines Django models `ImageGallery` and 'Image' representing gallery and gallery .
This model is associated with its respective database table specified in its `Meta` class.
"""
from django.db import models
from gallery.utils import image_upload_path
from account.models import User


class ImageGallery(models.Model):
    """
    The ImageGallery model with gallery name and foreign key to User model
    representing the user who owns the gallery.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='image_gallery_user_set')
    gallery_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.gallery_name)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the database table
        for ImageGallery model
        """
        db_table = 'ImageGallery'


class Image(models.Model):
    """
    The Image model with image name and foreign key to ImageGallery model
    representing the gallery in which image is uploaded.
    """
    image_gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE,
                                      related_name='image_gallery_set')
    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.image)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Use the Meta class to specify the database table
        for Image model
        """
        db_table = 'Image'
