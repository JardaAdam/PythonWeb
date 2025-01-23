from .base import *

DEBUG = True

# DEBUG = False   # pro testy accounts/tests/test_urls.py
# TEMPLATES[0]['OPTIONS']['debug'] = False

# In-memory databáze pro rychlost při běhu testů
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',  # Můžete použít ':memory:' pro čistě paměťovou DB
    }
}

# Testovací media root
MEDIA_ROOT = BASE_DIR / 'test_media'
MEDIA_URL = '/media_test/'

# Statické soubory. Pro testování můžete mít jinou strukturu.
STATIC_URL = '/static_test/'

# Optimalizace hashe hesel pro testy
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Rychlý backend mailu pro testovací účely
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'