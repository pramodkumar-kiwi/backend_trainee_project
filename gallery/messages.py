"""
This file contains VALIDATIONS & SUCCESS_MESSAGES which can be
imported to other files
"""
VALIDATION = {
    'video_gallery_name': {
        "blank": "Video Gallery name can not be blank",
        "required": "Please provide a name to video gallery",
        "exists": "Video Gallery with this name already exists",
        "exists_while_updating": "A video gallery with this name already exists for the current user."
    },

    'video': {
        "required": "Please provide a video",
        "video-format": "Only MP4 video files are supported"
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
    "VIDEO_GALLERY": {
        "CREATED_SUCCESSFULLY": "Video Gallery created successfully",
        "UPDATED_SUCCESSFULLY": "Video Gallery updated successfully",
        "DELETED_SUCCESSFULLY": "Video Gallery deleted successfully",
    },
    "VIDEO": {
        "CREATED_SUCCESSFULLY": "Video uploaded successfully",
        "DELETED_SUCCESSFULLY": "Video deleted successfully",
    }
}
