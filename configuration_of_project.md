## Klíčové Aspekty Konfigurace Django Projektu

### 1. Rozdělení Nastavení

- **`settings/base.py`**: Obsahuje společná nastavení pro všechna prostředí.
- **`settings/development.py`**: Specifická nastavení pro vývoj, včetně `DEBUG=True` a SQLite databáze.
- **`settings/production.py`**: Specifická nastavení pro produkci s bezpečnostními úpravami.
- **`settings/testing.py`**: Specifická nastavení pro testování s in-memory databází.

### 2. `urls.py` a Použití `settings`

- Při použití `urlpatterns` a přidávání statických a mediálních cest, využíváme `django.conf.settings` pro dynamické načítání nastavení v závislosti na prostředí.

### 3. `asgi.py` a `wsgi.py`

- Správná konfigurace `DJANGO_SETTINGS_MODULE` pro dynamické načítání správného prostředí.

### 4. Testování s `pytest-django`

- Použití `pytest.ini` k definování testovacího prostředí.
- Dodržování konvencí přípona názvu souborů a tříd.

### 5. Modely a Šablony

- Modely používají `django.conf.settings` pro přímou kompatibilitu s prostředím.
- Ujistěte se, že cesty k šablonám jsou správně nakonfigurovány ve `TEMPLATES` v `base.py`.
