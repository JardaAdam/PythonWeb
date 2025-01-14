### Vysvětlení přidaných komponent

- **Formatters:** Jsou definovány dva formáty - jednoduchý a detailní pro různé účely.
- **Handlers:** 
  - `console`: Logy jsou mimořádné události (ERROR) se vypisují na konzoli.
  - `file`: Ukládá všechny úrovně logů od INFO nahoru do specifikovaného souboru `production.log`.
  - `mail_admins`: Automaticky zasílá email administratorům při výskytu chyb na úrovni ERROR. 
  Tento handler je vhodné mít v produkci.
  
- **Loggers:**
  - `root`: Hlavní logger, který zachytává a zpracovává logy na úrovni WARNING a výš a splní je všemi třemi handlery.
  - `django`: Zpracovává logy pro Django systém na úrovni INFO s propagací deaktivovanou.
  - `django.request`: Zaměřuje se na chyby v rámci HTTP requestů a umožňuje rychle identifikovat chyby provozem.

Nezapomeňte se ujistit, že cesta pro `logs/production.log` existuje nebo je program schopen ji vytvořit. 
A také, abyste měli nakonfigurované emaily administrátorů v nastavení Django, pokud používáte `mail_admins` handler.