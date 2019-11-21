""" common place strings"""
# status
STATUS_UNAUTHORIZED = '401 Unauthorized'
STATUS_TOKEN_EXPIRED = '419 Authentication Timeout'

# common response
RETRIEVED_SUCCESS = "Retrieved successfully!"

# Validation
INVALID_CREDENTIAL = "Invalid Credentials"
INVALID_PAYLOAD = "Invalid payload"
VERIFICATION_FAILED = 'Verification failed'
EMAIL_EXISTS = "Email already exists"
PHONE_EXISTS = "Phone number already exists"
INVALID_ROLE = "Invalid role type"
INVALID_EMAIL = "Invalid email format"
INVALID_REFERRAL_CODE = "Invalid referral code"
ALREADY_INVITED = '{} is already invited'
INVALID_DAY = 'Invalid Day'
INVALID_UUID_LIST = 'Invalid {} uuid(s)'

# Auth
UNAUTHORIZED = "Unauthorized"
INVALID_TOKEN = "Invalid token"
TOKEN_EXPIRED = "Authentication Timeout"
TOKEN_MISSING = "Token missing"
USED_TOKEN = "Token already used"
INCORRECT_OLD_PASSWORD = "Incorrect old password"
SAME_NEW_PASSWORD = "New password should not be same as old password"
PASSWORD_LENGTH_ERR = "Make sure your password is at lest 8 letters"
PASSWORD_NUMBER_ERR = "Make sure your password has a number in it"
PASSWORD_CAPS_ERR = "Make sure your password has a capital letter in it"
PASSWORD_SMALL_ERR = "Make sure your password has a small letter in it"
FORBIDDEN = '''User doesn't have sufficient permissions to perform this
               operation'''

# Users
EMAIL_MISSING = "Email field is missing"
ROLE_MISSING = "role field is missing"
PASSWORD_MISSING = "Password field is missing"
NEW_PASSWORD_MISSING = "New Password field is missing"
COUNTRY_NOT_FOUND = 'Country code not found'
PHONE_NO_MISSING = 'phone_no is missing'
EMAIL_EMPTY = 'At least one email address required'
EMAIL_NOT_EXISTS = "Given email doest not exists"
EMAIL_SENDING_FAILED = "Email sending failed"
EMAIL_ROLE_NOT_EXISTS = "Email with this role not exists"
USER_PHONE_NUMBER_EXISTS = 'User with this phone number already exists'
