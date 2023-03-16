"""
This file contains all constant values
"""
MAX_LENGTH = {
    'video_gallery_name': 20,
}
MIN_LENGTH = {
    'video_gallery_name': 3,
}
MAX_SIZE = {
    'max_size': 50 * 1024 * 1024,
}
MAX_LIMIT = {
    'max_limit': 10,
}
VIDEO_FORMAT = '.mp4'
VIDEO_UPLOAD_PATH = '{username}/video/{gallery_name}/{filename}'
VIDEO_FILENAME_FORMAT = "{username}-{gallery_name}-{day}-{month}-{year}-" \
                  "{hour}-{minute}-{second}-{microsecond}{extension}"

VIDEO_GALLERY_PATH = 'media/{username}/video/{gallery_name}'
VIDEO_URL_TEMPLATE = "{}{}"
VIDEO_PATH_TEMPLATE = "{}{}"

MEDIA_URL = "media/"
folder_name = {
    'VIDEO_folder_name': 'video'
}
video_extensions = ['mp4', 'mov', 'avi', 'wmv', 'flv']
media_name = {
              'VIDEO_media': 'video'}

gallery_field_name = {
    'Video_gallery_field': 'video_gallery'

}