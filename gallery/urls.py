"""
This file contains URL patterns for a web app that serves gallery galleries and images.
It uses a DefaultRouter to generate views and serves uploaded images
from the media directory specified in project settings.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from gallery import views

router = DefaultRouter()
router.register('image-gallery', views.ImageGalleryViewSet, basename='image-gallery')
router.register('images', views.ImageViewSet, basename='image')

urlpatterns = [
                  path('', include(router.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
