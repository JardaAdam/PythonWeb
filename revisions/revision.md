### Vysvětlení modelů a funkcionality

- **MaterialType**: Udržuje možné typy materiálů, které lze snadno rozšířit o nové typy v budoucnosti.

- **Manufacturer**: Rozšířeno o životnost dle materiálu, což umožňuje dynamickou správu podle výrobce.

- **RevisionData**: Uchovává obecné informace o typech zařízení pro opakované použití.

- **RevisionRecord**: Uchovává detaily a historické záznamy pro jednotlivé OOPP, včetně automatické správy termínů revizí.

- **ItemGroup**: Umožňuje spojovat jednotlivé majetky uživatelů pro sledování skupinového vlastnictví.

- **timezone**:
   - Pro práci s časovými zónami v Django využijete modul `django.utils.timezone`, který je součástí Django frameworku. Tento modul poskytuje funkce pro časové operace, které respektují nastavení časové zóny vaší aplikace.

- **timedelta**:
   - timedelta je součástí standardní knihovny Pythonu, konkrétně v modulu `datetime`. Používá se pro reprezentaci rozdílu mezi dvěma daty.


Tento návrh poskytuje robustní a flexibilní strukturu pro správu OOPP prostředků s automatizovanými procesy, které budou 
usnadňovat řízení životnosti a plánování další revize. Pro budoucí rozšíření o sledování a upozorňování vlastníků o konci 
platnosti revizí nebo výrobních vadách bude vhodné integrovat plánovače úloh nebo systémy upozornění 
(např. prostřednictvím e-mailu nebo jiných služeb notifikace).



### OneToOne
- přesun položky mezi ItemGroup

```python
def move_item_to_new_group(item_record, new_group):
    """ Přesuňte položku do nové skupiny, pokud je to nutné """
    if item_record.item_group != new_group:
        # Přesuňte položku do nové skupiny
        item_record.item_group = new_group
        item_record.save()  # Uložení změn databáze
        return True
    return False

# Příklad použití
# Získání instance RevisionRecord a nové instance ItemGroup
revision_record = RevisionRecord.objects.get(serial_number='123456')
new_item_group = ItemGroup.objects.get(name='Nová skupina')

# Pokus o přesun
moved = move_item_to_new_group(revision_record, new_item_group)
if moved:
    print("Položka byla úspěšně přesunuta do nové skupiny.")
else:
    print("Položka již byla ve správné skupině.")
```

### Použití při filtrování a řazení

V databázových dotazech pak můžete využít tyto vztahy k filtrování či řazení záznamů:

```python
# Příklad filtrování nebo řazení v RevisionRecord podle material_type přes vztah na Manufacturer
from revisions.models import RevisionRecord

# Filtrovat záznamy podle určitého typu materiálu
records_filtered_by_material = RevisionRecord.objects.filter(revision_data__manufacturer__material_type__name='Aluminum')

# Řadit záznamy podle jména výrobce a poté podle typu materiálu
ordered_records = RevisionRecord.objects.order_by('revision_data__manufacturer__name', 'revision_data__manufacturer__material_type__name')
```

### Vysvětlení

- **`related_name='manufacturers'`** v `Manufacturer`: Tento název bude použitý k přístupu ke všem výrobcům daného materiálu z pohledu `MaterialType`. Např. `material_type.manufacturers.all()`.

### Filtrovani podle jmena polozky

Díky vazbě přes `ForeignKey` můžete jednoduše filtrovat záznamy v `RevisionRecord` podle `name_ppe` v `RevisionData`:

```python
from revisions.models import RevisionRecord

# Filtrovat podle name_ppe
filtered_records = RevisionRecord.objects.filter(revision_data__name_ppe='Název PPE')
```

### Zajistěte:

- **Správná jména atributů**: Ověřte, že `name_ppe` je správně definované a že cesty přes ORM jsou správně zapsány (`revision_data__name_ppe`).
  
- **Tabulky a vazby**: Ujistěte se, že vztahy mezi modely jsou správně vytvořeny a že `foreignKey` na `RevisionData` je správně nastaven.

### filtr pomoci vyrobce a materialu 

- **Filtrování a řazení**: Umožňuje snadné filtrování přes ORM, např. aby bylo možné zobrazit všechny záznamy revizí spojené s určitým typem materiálu prostřednictvím vztahu:
  ```python
  RevisionRecord.objects.filter(revision_data__manufacturer__material_type__name='Some Material')
  ```
- **Čitelnost kódu**: Poskytuje pojmenování, které jasně ukazuje vztah mezi materiálem a výrobci, což usnadňuje údržbu kódu.
