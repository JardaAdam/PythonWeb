## Django Tahák: Administration, Content Types a Sessions

# Administration | Log Entry

- **Účel**: Automatický záznam akcí prováděných uživateli v admin panelu (přidání, úpravy, mazání).
- **Co monitorovat**:
  - Kdo akci provedl
  - Co a kdy bylo změněno
  - Typ akce (přidání, změna, smazání)
- **Použití**: Umožňuje auditování a sledování změn pro lepší zabezpečení a správu dat.


**Django Admin Log Entry** je vestavěná funkce, která automaticky zaznamenává činnosti provedené uživateli ve 
správcovském rozhraní Django. Tento protokol se týká každé akce provedené v admin panelu, jako je přidání, 
úprava nebo smazání záznamu.

#### Příklad použití Admin Log Entry

**Sledování změn**

Představte si, že máte systém, kde je důležité sledovat, kdo provádí jaké úpravy dat. Může to být užitečné pro účely 
auditu nebo sledování, zda nějaké chyby nebyly způsobeny konkrétními úpravami.

1. **Scénář**: Revizní technik provede úpravu v záznamu `RevisionRecord`.

2. **Záznam logu v Action Log**:

   - Když revizní technik změní stav `RevisionRecord`, například aktualizuje datum revize, Django automaticky vytvoří záznam v `Admin Log Entry`.
   - Tento záznam obsahuje informace jako uživatel, čas provedení akce, typ akce (změna) a identifikaci objektu, který byl změněn.

3. **Zobrazení v admin panelu**:

   - Správci mohou vidět protokol akcí v rámci Django admin rozhraní tím, že přejdou na aplikaci, která ukládá tyto záznamy.
   - Lze prohlížet, kdo provedl kterou akci, kdy byla akce provedena a jaké konkrétní změny byly provedeny.

4. **Příklad v kódu: Zachycení změny**:

    Bez nutnosti zásahu uživatele Django automaticky spravuje logvý záznam. Pokud však chceme něco přizpůsobit, 
můžeme využít signály:

```python
from django.db.models.signals import post_save, pre_delete
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

def log_revision_change(sender, instance, **kwargs):
    if kwargs['created']:
        action_flag = ADDITION
    else:
        action_flag = CHANGE

    LogEntry.objects.log_action(
        user_id=instance.modified_by_id,
        content_type_id=ContentType.objects.get_for_model(instance).pk,
        object_id=instance.pk,
        object_repr=str(instance),
        action_flag=action_flag,
        change_message="Custom change made in RevisionRecord."
    )

post_save.connect(log_revision_change, sender=RevisionRecord)
```

**Výhody**:

- **Audit a sledovatelnost**: Snadný audit toho, co se přesně změnilo a kdy.
- **Bezpečnost**: Záznamy mohou sloužit k identifikaci neautorizovaných změn nebo poruch systému.
- **Historie**: Správci mají přístup k historickým datům o aktivitách v systému.

Tento záznam pomocí `Admin Log Entry` poskytuje důležitou vrstvu pro sledování a auditování činností ve vašem systému, 
což může být zásadní pro komplexnější aplikace, kde se sdílí a spravují citlivá data.

# Content Types

- **Účel**: Identifikace a správa různých modelů v rámci projektu. Umožňuje generický přístup k modelům.
- **Použití**:
  - **Generické vztahy**: Schopnost vztahovat objekty k libovolným modelům (např. komentáře k různým modelům).
  - Zajistit jednotnou správu oprávnění nad různými modely.

### Content Types v Django

**Content Types** jsou součástí vestavěného systému Django pro řešení modelů a jejich instance. Tento systém používá `django.contrib.contenttypes`, což je aplikace, která umožňuje generické modely – modely, které mohou pracovat s instancemi jakéhokoli jiného modelu. Content Types se používají k identifikaci a práci s jakýmkoli Django modelem bez ohledu na to, o jaký model se jedná.

### Usage of Content Types

Content Types mapují každý model k určitému klíčovému slovu (nebo identifikátoru). Například, pokud máš model `Book`, Django vytvoří instanci ContentType pro tento model. Ta instance může být používána k tomu, aby odkazovala na konkrétní model `Book` bez potřeby mít jeho skutečný modelový objekt.

### Permissions for Content Types

Když mluvíš o oprávněních jako „Can add content type“, „Can change content type“, atd., mluvíš o standardních akcích, které Django povoluje nad modely: 

- **Can add...** – Umožňuje uživateli přidávat nové instance určitého modelu.
- **Can change...** – Umožňuje uživateli měnit existující instance určitého modelu.
- **Can delete...** – Umožňuje uživateli mazat existující instance určitého modelu.
- **Can view...** – Umožňuje uživateli vidět (číst) existující instance určitého modelu.

### Kde tyto oprávnění najdu?

1. **Django Admin Panel**: Můžeš vidět všechna tato oprávnění v rámci Django admin panelu, když procházíš konfigurací oprávnění pro jednotlivé role (jako jsou Groups, nebo individuální uživatelé):

    1. Naviguj na Admin panel.
    2. Jdi do sekce Users nebo Groups.
    3. Přiřaď oprávnění jednotlivým uživatelům nebo skupinám.
    4. Uvidíš různé typy oprávnění pro různé modely, včetně těch pro Content Types.

2. **Database**: Oprávnění jsou uložena v databázi a mohou být přímo viděna v tabulce `auth_permission`.

3. **Terminal/Command Line**: Pokud používaš shell pro práci s Django, můžeš zkoumat oprávnění přímo skrz Django ORM:

```python
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get(app_label='contenttypes', model='contenttype')
permissions = Permission.objects.filter(content_type=content_type)

for perm in permissions:
    print(perm.name)
```

Tento kód zobrazuje všechna specifická oprávnění pro `contenttypes` aplikaci.

### Případ použití Content Types v Django Permissions

V kontextu, který jste popsal výše, pro různé role uživatelů a řízení přístupu v aplikaci, se použití Content Types 
může hodit zejména v případech, kdy potřebujete implementovat **generická oprávnění** nebo 
**operace napříč různými typy modelů**.

#### Příklad použití Content Types

**Generické komentáře**

Pokud chcete implementovat systém komentářů, kde uživatelé mohou přidávat komentáře k libovolným typům záznamů 
(např. `RevisionRecord`, `Company`, atd.), můžete použít Content Types pro univerzální řešení. 

1. **Modelový návrh s Content Types**:

```python
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

2. **Použití v praxi**: Uživatel může přidávat komentáře k libovolným objektům, např. ke konkrétním `RevisionRecord` nebo `Company`.

```python
from django.contrib.contenttypes.models import ContentType

revision_record = RevisionRecord.objects.get(pk=1)
content_type = ContentType.objects.get_for_model(revision_record)

comment = Comment.objects.create(
    user=user_instance,
    content_type=content_type,
    object_id=revision_record.id,
    text="This is my comment on this revision record."
)
```

**Důvod použití**: Pomocí Content Types lze snadno spravovat vztahy napříč různorodými modely bez potřeby psát 
specializovaný kód pro každý jednotlivý model. To umožňuje efektivnější správu vztahů a operací v aplikace, 
která pracuje s různými datovými objekty.

Tato flexibilita se může hodit zejména v aplikacích s širokým spektrem datových typů, kde chcete aplikovat 
společné operace (např. komentování, hodnocení, sledování) na všech záznamech bez ohledu na jejich základní typ.



  
# Sessions

- **Účel**: Uložení relací uživatele za účelem uchovávání dat napříč requesty. 
- **Složky**:
  - **Session Key**: Identifikační klíč pro každou relaci.
  - **Session Data**: Data uložena na serveru pro konkrétní relaci.
  - **Expire Date**: Datum, kdy se relace automaticky ukončí.
- **Použití**: 
  - Udržení stavu (např. přihlášení uživatele, obsah košíku).
  - Zabezpečení a správa aktivních relací v aplikaci.

**Django Sessions** jsou způsob, jak ukládat data specifická pro návštěvníka webové stránky nebo uživatelskou relaci. 
To umožňuje serveru udržet informace o uživateli napříč různými requesty a interakci s webem. 

### Jak to funguje:

1. **ID relace**: Při každém navázání nové relace (např. při prvním přihlášení uživatele) je vytvořeno unikátní 
2. identifikační číslo relace (session ID), které je zasláno klientovi (obvykle jako cookie).

2. **Ukládání dat**: Server pak může s tímto ID spojit různé informace, jako je stav uživatelova přihlášení,
obsah jeho košíku, nastavení jazykové verze atd.

3. **Django Session framework**: Django používá svůj framework pro relace, který automatizuje správu session 
ID a ukládání relací do úložiště (buď do databáze, do cache nebo do souborového úložiště).

### Sessions v Admin panelu

V admin panelu Django můžeš na úrovni superuživatele sledovat aktivní relace ve své aplikaci. To znamená, 
že můžeš zobrazit všechny současné relace uživatelů, které jsou uloženy na serveru.

#### Co najdeš v sekci „Sessions“:

1. **Session Key**: Jedinečný klíč ID relace, který identifikuje konkrétní relaci.

2. **Session Data**: Uložená data pro session, což může obsahovat například ID uživatele, pokud je přihlášen.

3. **Expire Date**: Datum a čas, kdy bude relace automaticky odstraněna, pokud nebude obnovena novým requestem.

#### Typické použití:

- **Bezpečnostní opatření**: Administrátor může například z bezpečnostních důvodů kontrolovat počet aktivních relací 
a podle toho uzavírat relace například při podezření na neobvyklou aktivitu.
  
- **Rychlá práce s relacemi**: Možnost manuálně spravovat či „ukončit“ relace v případě potřeby.

Django Sessions je tedy velmi výkonný nástroj pro sledování a správu uživatelských relací, což je nezbytné pro 
udržení stavu a personalizace uživatelského zážitku na webu. Při přístupu jako superuživatel v admin rozhraní můžeš 
vidět všechny tyto detaily, což ti umožní lépe spravovat a monitorovat, jak uživatelé interagují s tvojí aplikací.