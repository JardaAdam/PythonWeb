# Konfigurace Django prostředí

Tento dokument popisuje strukturu a důvody pro rozdělení konfiguračních souborů v Django projektu. Cílem je zajistit, 
aby byla konfigurace jasně oddělená pro různé typy nasazení: vývojové, testovací a produkční. Tento přístup zajišťuje, 
že každé prostředí má přesně to, co potřebuje, aniž by ohrozilo bezpečnost nebo stabilitu ostatních prostředí.

## Proč oddělit konfigurační soubory?

Rozdělení konfiguračních souborů podle prostředí přináší několika výhod:

1. **Bezpečnost**: Citlivá data, jako jsou klíče nebo přihlašovací údaje do databáze, jsou izolována a nejsou přímo 
součástí verzovacího systému.
2. **Přehlednost**: Nastavení jsou organizována přehledně a je snadné je na první pohled pochopit.
3. **Flexibilita**: Každé prostředí může mít specifickou konfiguraci pro svou potřebu (např. výkonová optimalizace v 
produkci vs. ladění ve vývoji).
4. **Izolace problémů**: Testovací a vývojová prostředí mohou být změněna bez obavy, že způsobí problémy v produkci.

## Struktura konfiguračních souborů

### `base.py`
- **Popis**: Základní nastavení platná pro všechna prostředí. Obsahuje společné knihovny, aplikace, middleware a další 
nezbytné komponenty.
- **Obsahuje**:
  - Instalované aplikace (`INSTALLED_APPS`)
  - Definice middleware (`MIDDLEWARE`)
  - Šablony a URL konfigurace (`TEMPLATES`, `ROOT_URLCONF`)
  - Ověřování hesel (`AUTH_PASSWORD_VALIDATORS`)
  - Jazyková a časová nastavení (`LANGUAGE_CODE`, `TIME_ZONE`)

### `development.py`
- **Popis**: Konfigurace pro vývojové prostředí, kde je aktivní ladění a používá se lokální databáze.
- **Klíčové body**:
  - `DEBUG = True` pro detailní hlášení chyb
  - SQLite pro snadný lokalní vývoj
  - Lokální media root pro uživatelské soubory

### `production.py`
- **Popis**: Konfigurace pro produkční nasazení, kde je důraz kladen na bezpečnost a výkon.
- **Klíčové body**:
  - `DEBUG = False` pro minimalizaci úniku informací
  - Ochrana na úrovni hostitelů a bezpečnostní hlavičky
  - Nastavení pro robustní databázi, např. PostgreSQL

### `testing.py`
- **Popis**: Nastavení pro testovací prostředí, se zaměřením na rychlost a izolaci testů.
- **Klíčové body**:
  - Rychlejší hashování hesel pro urychlení testů
  - Locmem backend pro e-maily
  - Izolovaná databáze pro testovací účely

## Další kroky

- Ujistěte se, že máte správně nastaveny proměnné prostředí, zejména pro `SECRET_KEY` a připojení k databázi.
- Používejte verzi `.env` souboru pro ukládání citlivých konfigurací, které se nenačítají mechanizmem verzovacího systému.

Tento přístup poskytuje stabilní a bezpečný rámec pro rozvoj a nasazení, přičemž zajišťuje, že rozdělení odpovědnosti 
mezi různá prostředí je systematické a škálovatelné.