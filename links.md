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

## Zálohování databáze Export (DUMP):
```bash
python manage.py dumpdata > backup.json
```
## Načítání ze zalohy Import (LOAD):
```bash
python manage.py loaddatautf8 ./files/fixtures.json
```
## Spuštění testů
```bash
python manage.py test
```


## Aktualizace slozky s balicky
```bash
pip freeze > requirements.txt
```

## ? 
```bash
python manage.py shell
```

