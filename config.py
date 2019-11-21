""" config values """
import os
from flask.cli import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv('LOG_LEVEL', 'ERROR')

# DB Config
DB_URL = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.getenv('POSTGRES_USER', ''),
    os.getenv('POSTGRES_PASSWORD', ''),
    os.getenv('POSTGRES_HOST', ''),
    os.getenv('POSTGRES_PORT', '5432'),
    os.getenv('POSTGRES_DB', ''))

DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '10'))
DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '-1'))

# API
API_PREFIX = os.getenv('API_PREFIX', '/api/v')
REFERRAL_CODE_LENGTH = 6
JSON_SORT_KEYS = False

# Auth
JWT_ALGORITHM = "HS256"
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_BLACKLIST_TOKEN_CHECKS = [
    '/signup', '/login', '/token/refresh', '/payments/status',
    '/history/download', '/reset-password', '/forgot-password',
    '/orders/pos', '/by-vendor/download', '/schools/search', '/status']

JWT_ACCESS_TOKEN_TIMEOUT_MINUTES = int(
    os.getenv('JWT_ACCESS_TOKEN_TIMEOUT_MINUTES', '60'))
JWT_REFRESH_TOKEN_TIMEOUT_MINUTES = int(
    os.getenv('JWT_REFRESH_TOKEN_TIMEOUT_MINUTES', '600'))
ENABLE_AUTH = bool(os.getenv('ENABLE_AUTH', 'False') == 'True')
PASSWORD_LENGTH = int(os.getenv('PASSWORD_LENGTH', '8'))
