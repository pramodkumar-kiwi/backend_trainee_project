"""
This file contains the validation, success and error
messages to provide as constants messages.
"""

SIGNUP_VALIDATION_ERROR = {
    'first_name': {
        "blank": "first name can not be blank",
        "invalid": "first name must contain only alphabets",
        "required": "first name required",
    },
    'last_name': {
        "blank": "last name can not be blank",
        "invalid": "last name must contains only alphabets",
        "required": "last name required",
    },
    'username': {
        "blank": "username can not be blank",
        "invalid": "username must contain alphabet and special character",
        "required": "username required",
        "exits": "username already exist"
    },
    'email': {
        "blank": "Email can not be blank",
        "required": "Email required",
        "exits": "email already exist"
    },
    'contact': {
        "blank": "contact can not be blank",
        "required": "contact required",
        "invalid": "invalid contact"
    },
    'password': {
        "blank": "password can not be blank",
        "invalid": "Password must contain uppercase, lowercase, digit and special character",
        "required": "password required"
    },

}

SIGNIN_VALIDATION_ERROR = {
    'username': {
        "blank": "username can not be blank",
        "invalid": "username must contain alphabet and special character",
        "required": "username required",
        "exits": "username already exist"
    },
    'password': {
        "blank": "password can not be blank",
        "invalid": "Password must contain uppercase, lowercase, digit and special character",
        "required": "password required"
    },
    "invalid credentials": "Invalid Credentials",
}

EMAIL_VALIDATOR_VALIDATION_ERROR = {
    'email': {
        "blank": "email can not be blank",
        "required": "email required",
        "exits": "email already exist"
    }
}

USERNAME_VALIDATOR_VALIDATION_ERROR = {
    'username': {
        "blank": "username can not be blank",
        "required": "username required",
        "exits": "username exist"
    }
}

TOKEN_ERROR = {
    'Invalid': "Invalid Token",
}

SUCCESS_MESSAGE = {
    'success': "Updated Successfully"
}

ERROR_MESSAGE = {
    'error': "Update Failed"
}

FORGET_PASSWORD = {
    'email': {
        'email_sent': 'Password reset email sent',
        'email_failed': 'Email verification failed',
        'email_not_exist': "Email does not exist",
        'link_expired': 'Forget password link expired. '
                        'Please submit the forget password form again.'
    },
}

RESET_PASSWORD = {
    'password_reset': {
        'successful': 'Password reset successful',
        'fail': 'Invalid password',
        'do_not_match': 'Passwords do not match'

    },
    'token': {
        'invalid': 'Invalid token',
        'expired': 'Your token has been expired',
    }
}
