from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from image import views

# Creating Router Object
router = DefaultRouter()

"""
Routing for Image-Gallery
"""

router.register('image-gallery', views.ImageGalleryViewSet, basename='image-gallery')


urlpatterns = [
                  path('', include(router.urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)