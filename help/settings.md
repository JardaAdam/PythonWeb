## uprava DATABASES 

### pouziti jine database
```python


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME", default="db"),
        'USER': os.getenv("DB_USER", default="user1"),
        'PASSWORD': os.getenv("DB_PASSWORD", default="12345"),
        'HOST': os.getenv("DB_HOST", default="localhost"),
        'PORT': os.getenv("DB_PORT", default="1234"),
    }
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'DATABASE': os.getenv("DB_NAME", default="db"),
        'USER': os.getenv("DB_USER", default="user1"),
        'PASSWORD': os.getenv("DB_PASSWORD", default="12345"),
        'HOST': os.getenv("DB_HOST", default="localhost"),
        'PORT': os.getenv("DB_PORT", default="1234"),
```
- .env ulozeni pristupove data
```bash
DB_NAME=hollymovies
DB_USER=admin
DB_PASSWORD=mojetajneheslo
DB_HOST=localhost
DB_PORT=5432
```

### pro testy 
```python
import sys

if 'test' in sys.argv:  # FIXME
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
```
- timto zapisem muzu nastavit databazi pro testy musim ale vytvorit kopii sve databaze a prejmenovat ji 
  - viz posledni radek -> 'test_db.sqlite3'
  - a pridat do .gitignore -> /test_db.sqlite3