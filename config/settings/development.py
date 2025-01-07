from .base import *

DEBUG = True

ALLOWED_HOSTS = []


# Databáze - SQLite pro jednoduchost při vývoji
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files (user-uploaded content)
MEDIA_ROOT = BASE_DIR
MEDIA_URL = '/media/'

