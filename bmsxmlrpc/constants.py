# Standard-library imports...
import os


BASE_URL = 'http://127.0.0.1:8442'
SKIP_REAL = os.getenv('SKIP_REAL', True)
SKIP_TAGS = os.getenv('SKIP_TAGS', ['real'])
