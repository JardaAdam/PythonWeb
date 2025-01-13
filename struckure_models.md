### `accounts/models.py`

#### Model `Country`

- **`name`**: Název země, unikátní identifikátor.
- **`business_id_format`**: Regex formát pro validaci **business_id**.
- **`tax_id_format`**: Regex formát pro validaci daňových ID.
- **`tax_id_prefix`**: Defaultní prefix (např. "CZ") pro daňové ID dle země.
- **`phone_number_prefix`**: Předvolba pro telefonní čísla dané země.
- **`postcode_format`**: Regex formát pro validaci poštovních směrovacích čísel.

#### Model `CustomUser`

- **Dědění z `AbstractUser`**: Využívá relevantní funkce a vlastnosti built-in uživatelského modelu Django.
- **`company_name`, `address`, `city`**: Ukládá další informace pro uživatele spojené s firmou.
- **`postcode`**: Formát poštovního směrovacího čísla s validací dle země.
- **`phone_number`**: Obsahuje předvolbu podle země, validace založená na zemi.
- **`business_id`**, **`tax_id`**: Ukládání identifikačních čísel s validací dle národních formátů.
- **`discount`**: Slevové procento pro uživatele.
- **`can_view_multiple_groups`**: Boolean, který určuje přístup uživatele ke skupinám.
- **`country`**: Odkazuje na `Country` pro komplexní geografickou validaci.
- **Meta a Přístupové metody**:
  - **`ordering`**: Určení výchozího řazení.
  - **`clean()`**: Implementuje validace na základě zvoleného státu uživatele.


#### Model `ItemGroup`

- **`name`**: Název skupiny položek.
- **`user`**: Cizí klíč na `CustomUser`, vlastníka skupiny.
- **`items`**: `ManyToManyField` na `RevisionRecord`, propojuje více položek se skupinou.

### `calculator/models.py`

### Model `CalculatorOutput`

- **`customer`**:
  - Cizí klíč na `CustomUser`, reprezentuje zákazníka, který udělal objednávku.
  - `related_name='orders'`: Umožňuje přístup k objednávkám daného uživatele jako `user.orders.all()`.
  - `related_query_name='custom_order'`: Pro usnadnění vyhledání, například `CustomUser.objects.filter(custom_order__total_price__gt=100)`.

- **`created`**: Automaticky nastavené datum a čas, kdy byla objednávka vytvořena.
- **`updated`**: Automaticky aktualizované datum a čas při každém uložení objednávky.
- **`is_submitted`**: Boolean indikátor, zda byla objednávka odeslána/finalizována.
- **`total_price_revision`**: cena ze položky v revizi
- **`total_price_transport`**: cena za dopravu k zakaznikovy/ přepravní služba
- **`total_price`**: Celková cena za objednávku, vykalkulovaná na základě položek a jejich cen.



- **`calculate_total()`**:
  - Metoda počítá celkovou cenu všech položek v objednávce a aktualizuje pole `total_price`.
  - Prochází všechny položky v `CalculatorItem` spojené s objednávkou a násobí množství s cenou jednotlivých typů OOP.

### Model `CalculatorItem`

- **`calculator`**: Cizí klíč na `CalculatorOutput`, ke kterému položka objednávky náleží.
  - `related_name='calculatoritems'`: Poskytuje přístup z objednávky k jejím položkám jako `order.calculatoritems.all()`.

- **`type_of_ppe`**: Cizí klíč na `TypeOfPpe`, definuje typ ochranného prostředku v položce objednávky.

- **`quantity`**: Integer pole, které udává množství daného typu OOP ve zvolené objednávce. Zadává Customer
  - Validováno pomocí `MinValueValidator(0)` pro zajištění, že hodnota nemůže být negativní.



### Shrnutí modelů v aplikaci `calculator`:

Tyto modely slouží k vytvoření základního systému pro správu objednávek v rámci platformy, 
kde každý uživatel (`CustomUser`) může vytvářet objednávky (`CalculatorOutput`) obsahující jednu nebo více 
položek ochranných prostředků (OOP), které jsou konkrétně specifikovány v `CalculatorItem`. Systém je navržen tak, 
aby flexibilně podporoval revizi a úpravu objednávek, přičemž poskytuje přesné vedení účtování s ohledem na množství a 
typ použitých prostředků.



### `revision/models.py`

#### Model `MaterialType` 
- **`symbol`**: 
- **`name`**: Typ materiálu (např. Textile, Helmet, Harness, Ropes).

### Model `StandardPpe`
- **`image`**:
- **`code`**:
- **`description`**:

#### Model `Manufacturer`
- **`logo`**:
- **`name`**: Jméno výrobce.

### Model `LifetimeOfPpe`
- **`manufacturer`**:
- **`material_type`**: Odkazuje na `MaterialType`.
- **`lifetime_use_years`**: Maximální doba používání od data prvního použití.
- **`lifetime_manufacture_years`**: Maximální doba od data výroby.

#### Model `TypeOfPpe` 
- **`image`**:
- **`group_type_ppe`**: Identifikuje skupinu OOP (osobních ochranných prostředků).
- **`price`**: Cena asociovaná se skupinou PPE.


#### Model `RevisionData`

- **`image_items`**: Obrázek spojený s typem revize.
- **`lifetime_of_ppe`**: Odkazuje na `lifetime_of_ppe`.
- **`type_of_ppe`**: Odkazuje na `TypeOfPpe`.
- **`name_ppe`**: jméno ochranného prostředku.
- **`standard_ppe`**: norma ochranného prostředku.
- **`manual_for_revision`**: Manuál k revizi.
- **`notes`**:

#### Model `RevisionRecord`
- **`photo_of_item`**:
- **`revision_data`**: Odkazuje na `RevisionData`.
- **`serial_number`**: Unikátní sériové číslo.
- **`date_manufacture`**: Datum výroby
- **`date_of_first_use`**: Datum prvního použití.
- **`date_of_revision`**: Datum poslední revize.
- **`date_of_next_revision`**: Datum příští revize.
- **`owner`**: Odkazuje na `CustomUser`.
- **`item_group`**: Přiřazeno k `ItemGroup`.
- **`verdict`**: Hodnocení stavu položky.
- **`notes`**: Poznámky.
- **`created_by`**:
- **`created`**:
- **`updated`**:

### Obecné doporučení
1. **Pojmenování a konvence**: Udržujte konzistentní pojmenování proměnných a metod. To zlepší čitelnost a údržbu kódu.

2. **Použití verbose_name**: Pro lepší čitelnost v administraci Django zvážit použití `verbose_name` a `verbose_name_plural` pro všechny modely a pole.

3. **Dokumentace**: Podrobnější dokumentace tříd a metod pomůže v budoucnu s údržbou kódu.

### Optimalizace k jednotlivým modelům

#### `Country`

- **Validace regex**: Pokud používáte regex pro validaci formátů, ujistěte se, že jsou tyto regexy správně definované a testované, abyste se vyhnuli problémům při validaci.

#### `CustomUser`

- **Polymorfismus**: Zvážit použití přístupu, který umožňuje rozšíření uživatelské třídy bez nutnosti přímých vazeb, což by později mohlo váš kód udělat flexibilnější.
  
- **Mechanismus pro úpravy validací**: Namísto validací v metodě `clean` by bylo lepší přesunout tyto logiky do vlastních validatorů nebo manažerů pro lepší udržovatelnost a opakovatelnou použitelnost.

#### `ItemGroup`

- **Vazby na uživatele**: Zajistit, že vztah mezi `ItemGroup` a `CustomUser` je správně dimenzován podle obchodní logiky. Pokud několik uživatelů může mít společnou skupinu, zvážit změnu vazby na ManyToManyField.

#### `CalculatorOutput`

- **Navrhování na úrovni vazeb**: Zajištění, že použitými cizími klíči a vazbami se správně reflektují vztahy v databázi tak, aby efektivně zvládaly mazání nebo změny dat.

- **Logika pro výpočet ceny**: Otestovat logiku `calculate_total_revision` a zvažte, jak zajistit atomičnost a bezpečnost transakcí.

#### `RevisionRecord`

- **Výpočet data příští revize**: Ujistit se, že používáte správný časový interval pro specifikaci příští revize. Umožnit snadné změny dat (např. s pomocí konfigurace).

- **Úložné struktury pro poznámky**: Velká pole textových dat (např. `notes`) by mohla ovlivnit paměť při četném přístupu v hromadných operacích. Zvážit optimalizaci pokud se prokáže jako úzké hrdlo.

#### Další úvahy

- **Indexování a dotazování**: Zvážit, kde mohou indexy na polích snížit zatížení dotazů (např. často filtrované pole).
  
- **Relace a referenční integrita**: Zajistit, že všechny vztahy jsou zohledněny - např. jakým způsobem bude propojena při smazání uživatele jeho data v `CalculatorOutput`.

- **Testování a chyby**: Testovat validace, migrace, a výkonnost na vzorcích reálných dat, aby se předešlo problémům po zavedení do produkce.