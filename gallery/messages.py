"""
This file defines dictionaries containing validation error messages and success messages
for the Image Gallery app.
The VALIDATION dictionary contains error messages for form validation,
while the SUCCESS_MESSAGES dictionary contains success messages for various operations in the app.
"""
VALIDATION = {
    'gallery_name': {
        "blank": "Gallery name can not be blank",
        "required": "Please provide a gallery name",
        "exists": "Gallery with this name already exists"
    },
    'image': {
        "required": "Please provide a image",
        "max_size": "Make sure the image size is less than 2 Mb",
        "no_image": "No images found"
    },
    'image_gallery_id': {
        "required": "Please provide a image gallery id",
    },
    'image_gallery_set': {
        'no_album': 'No album found',
        'max_limit': 'Cannot upload more than 10 images.',
        'available_slots': 'Make sure you have enough space in the gallery',
    }
}
SUCCESS_MESSAGES = {
    "IMAGE_GALLERY": {
        "CREATED_SUCCESSFULLY": "Gallery created successfully",
        "UPDATED_SUCCESSFULLY": "Gallery updated successfully",
        "DELETED_SUCCESSFULLY": "Gallery deleted successfully",
    },
    "IMAGE": {
        "CREATED_SUCCESSFULLY": "Image uploaded successfully",
        "DELETED_SUCCESSFULLY": "Image deleted successfully",
    },
}
ERROR_MESSAGES = {
    'IMAGE': {
        'NO_IMAGE': "This Gallery is empty"
    }
}
