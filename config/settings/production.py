from .base import *

DEBUG = False

# TODO Nahradit skutecnou domenou
ALLOWED_HOSTS = ['.yourproductiondomain.com']

# Databázová konfigurace pro produkci (například PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'producedb'),
        'USER': os.getenv('DB_USER', 'produceuser'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'securepassword'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media root pro produkci
# TODO nekdere soubory z development jsou jiz pripraveny jako soubory do produkce upravit !!
MEDIA_ROOT = BASE_DIR / 'production_media'

# Bezpečnostní hlavičky
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

