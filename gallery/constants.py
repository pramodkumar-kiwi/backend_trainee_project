"""
This file contains various constants used throughout the module.
These constants define the maximum and minimum length of the gallery name,
maximum limit of images in a gallery, maximum size of gallery,
and the template paths for gallery and gallery upload.
The filename format for an uploaded gallery is also defined in this block.
"""

MAX_LENGTH = {
    'gallery_name': 20,
}
MIN_LENGTH = {
    'gallery_name': 5,
}
MAX_LIMIT = {
    'max_limit': 10,
}
MAX_SIZE_IMAGE = {
    'max_size': 2 * 1024 * 1024,
}

MAX_SIZE_VIDEO = {
    'max_size': 10 * 1024 * 1024,
}

MEDIA_URL = "media/"

IMAGE_URL_TEMPLATE = "{}{}"
IMAGE_PATH_TEMPLATE = "{}{}"

IMAGE_GALLERY_PATH = 'media/{username}/image/{gallery_name}'

IMAGE_UPLOAD_PATH = "{username}/image/{gallery_name}/{filename}"

FILENAME_FORMAT = "{username}-{gallery_name}-{day}-{month}-{year}-" \
                  "{hour}-{minute}-{second}-{microsecond}{extension}"

IMAGE_GALLERY = '{username}/image/{gallery_name}'