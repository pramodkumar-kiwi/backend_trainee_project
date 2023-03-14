"""
This file contains urls for gallery app and
register routers.
The defined urls in gallery app are image-gallery,video-gallery,image and video
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gallery import views

router = DefaultRouter()

"""
Routing for image-gallery,video-gallery,image and video
"""
router.register('image-gallery', views.ImageGalleryViewSet, basename='image-gallery')
router.register('video-gallery', views.VideoGalleryViewSet, basename='video-gallery')
router.register('image', views.ImageViewSet, basename='image')
router.register('video', views.VideoViewSet, basename='video')

urlpatterns = [
                  path('', include(router.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
