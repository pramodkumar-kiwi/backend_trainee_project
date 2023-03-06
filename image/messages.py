"""
This file contains VALIDATIONS & SUCCESS_MESSAGES which can be
imported to other files
"""
VALIDATION = {
    'gallery_name': {
        "blank": "Gallery name can not be blank",
        "required": "Please provide a gallery name",
    },
    'image': {
        "required": "Please provide a image",
    },
    'image_gallery_id': {
        "required": "Please provide a image gallery id",
        },
    'image_gallery_set': {
        'no_album': 'No album found',
        'max_limit': 'A gallery can have no more than 10 images.',
    }
}

SUCCESS_MESSAGES = {
    "IMAGE_GALLERY": {
        "CREATED_SUCCESSFULLY": "Image Gallery created successfully",
        "UPDATED_SUCCESSFULLY": "Image Gallery updated successfully",
        "DELETED_SUCCESSFULLY": "Image Gallery deleted successfully",
    },
    "IMAGE": {
            "CREATED_SUCCESSFULLY": "Image uploaded successfully",
            "DELETED_SUCCESSFULLY": "Image deleted successfully",
        }
}
