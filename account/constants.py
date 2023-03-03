"""
It contains all constant values
"""
REGEX = {
    "first_name": r'^[a-zA-Z]+$',
    "last_name": r'^[a-zA-Z]+$',
    "USERNAME": r'/^(?=.{8})[a-z][a-z\d]*@$',
    "contact": r'^\d+$',
    "PASSWORD": r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+=-])[0-9a-zA-Z!@#$%^&*()_+=-]{8,16}$',
}
