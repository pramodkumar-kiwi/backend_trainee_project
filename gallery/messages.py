"""
This file contains VALIDATIONS & SUCCESS_MESSAGES which can be
imported to other files
"""
VALIDATION = {
    'image_gallery_name': {
        "blank": "Image Gallery name can not be blank",
        "required": "Please provide a name to image gallery",
    },
    'video_gallery_name': {
        "blank": "Video Gallery name can not be blank",
        "required": "Please provide a name to video gallery",
    },

    'image': {
        "required": "Please provide a image",
    },
    'video': {
        "required": "Please provide a video",
    },
    'image_gallery_id': {
        "required": "Please provide a image gallery id",
    },
    'image_gallery_set': {
        'no_album': 'No album found',
        'max_limit': 'Cannot upload more than 10 images.',
    },
    'video_gallery_id': {
        "required": "Please provide a video gallery id",
    },
    'video_gallery_set': {
        'no_album': 'No album found',
        'max_limit': 'Cannot upload more than 10 videos.',
    }
}

SUCCESS_MESSAGES = {
    "BASE_GALLERY": {
        "CREATED_SUCCESSFULLY": "Base Gallery created successfully",
        "UPDATED_SUCCESSFULLY": "Base Gallery updated successfully",
        "DELETED_SUCCESSFULLY": "Base Gallery deleted successfully",
    },
    "IMAGE": {
        "CREATED_SUCCESSFULLY": "Image uploaded successfully",
        "DELETED_SUCCESSFULLY": "Image deleted successfully",
    },
    "VIDEO": {
        "CREATED_SUCCESSFULLY": "Video uploaded successfully",
        "DELETED_SUCCESSFULLY": "Video deleted successfully",
    }
}
