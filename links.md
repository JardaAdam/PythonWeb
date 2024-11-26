# zalozeni projekty Django
- Vytvoření virtuálního prostředí
```bash
python -m venv .venv
```
- Aktivace prostředí na Windows
```bash
.venv\Scripts\activate
```

## Instalace Django a dalších potřebných knihoven

```bash
pip install django python-dotenv
```
- Vytvoření nového projektu
```bash
django-admin startproject <nazev> .
```
- Vytvoření nové aplikace
```bash
python manage.py startapp <aplikace>
```
## Vytvoření superuživatele
```bash
python manage.py createsuperuser
```

## Migrace 
- Připravit migrace: Připraví změny v modelu a uloží je do migračních souborů.
```bash 
python manage.py makemigrations
```
- Inicializace tabulek v databázi: Aplikuje tyto změny na databázi (např. vytvoření tabulek, přidání sloupců)
```bash
python manage.py migrate
```
- Seznam migrací
```bash
python manage.py showmigrations
```

# Zálohování a testování
## Zálohování databáze
```bash
python manage.py dumpdata > backup.json

```
## Spuštění testů
```bash
python manage.py test
```


##aktualizace slozky s balicky
```bash
pip freeze > requirements.txt
```

