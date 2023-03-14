"""
This file contains all constant values
"""
MAX_LENGTH = {
    'image_gallery_name': 20,
    'video_gallery_name': 20,
}
MIN_LENGTH = {
    'image_gallery_name': 3,
    'video_gallery_name': 3,
}
MAX_SIZE = {
    'max_size': 2 * 1024 * 1024,
}

IMAGE_UPLOAD_PATH = "{username}/image/{gallery_name}/{filename}"
VIDEO_UPLOAD_PATH = '{username}/video/{gallery_name}/{filename}'
IMAGE_FILENAME_FORMAT = "{username}-{gallery_name}-{image_count_str}-{day}-{month}-{year}-" \
                        "{hour}-{minute}-{second}-{microsecond}{extension}"
VIDEO_FILENAME_FORMAT = "{username}-{gallery_name}-{video_count_str}-{day}-{month}-{year}-" \
                        "{hour}-{minute}-{second}-{microsecond}{extension}"
folder_name = {
    'VIDEO_folder_name': 'video',
    'IMAGE_folder_name': 'image'}

media_name = {'IMAGE_media': 'image',
              'VIDEO_media': 'video'}

gallery_field_name={
    'Image_gallery_field': 'image_gallery',
    'Video_gallery_field': 'video_gallery'

}