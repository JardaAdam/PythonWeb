### `accounts/models.py`

#### Model `Country`

- **`name`**: Název země, unikátní identifikátor.
- **`business_id_format`**: Regex formát pro validaci firemních ID.
- **`tax_id_format`**: Regex formát pro validaci daňových ID.
- **`tax_id_prefix`**: Defaultní prefix (např. "CZ") pro daňové ID.
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
  - **`__repr__`** a **`__str__`**: Zajišťují čitelnou reprezentaci uživatelských dat.

#### Model `ItemGroup`

- **`name`**: Název skupiny položek.
- **`user`**: Cizí klíč na `CustomUser`, vlastníka skupiny.
- **`items`**: `ManyToManyField` na `RevisionRecord`, propojuje více položek se skupinou.
- **`__str__`**: Textově reprezentuje objekt s detailními informacemi.

### `calculator/models.py`

### Model `CalculatorOutput`

- **`customer`**:
  - Cizí klíč na `CustomUser`, reprezentuje zákazníka, který udělal objednávku.
  - `related_name='orders'`: Umožňuje přístup k objednávkám daného uživatele jako `user.orders.all()`.
  - `related_query_name='custom_order'`: Pro usnadnění vyhledání, například `CustomUser.objects.filter(custom_order__total_price__gt=100)`.

- **`created`**:
  - Automaticky nastavené datum a čas, kdy byla objednávka vytvořena.

- **`updated`**:
  - Automaticky aktualizované datum a čas při každém uložení objednávky.

- **`is_submitted`**:
  - Boolean indikátor, zda byla objednávka odeslána/finalizována.

- **`total_price`**:
  - Celková cena za objednávku, vykalkulovaná na základě položek a jejich cen.

- **`__str__`**:
  - Poskytuje textovou reprezentaci objednávky s uživatelským jménem a celkovou cenou.

- **`calculate_total()`**:
  - Metoda počítá celkovou cenu všech položek v objednávce a aktualizuje pole `total_price`.
  - Prochází všechny položky v `CalculatorItem` spojené s objednávkou a násobí množství s cenou jednotlivých typů OOP.

### Model `CalculatorItem`

- **`calculator`**:
  - Cizí klíč na `CalculatorOutput`, ke kterému položka objednávky náleží.
  - `related_name='calculatoritems'`: Poskytuje přístup z objednávky k jejím položkám jako `order.calculatoritems.all()`.

- **`type_of_ppe`**:
  - Cizí klíč na `TypeOfPpe`, definuje typ ochranného prostředku v položce objednávky.

- **`quantity`**:
  - Integer pole, které udává množství daného typu OOP ve zvolené objednávce.
  - Validováno pomocí `MinValueValidator(0)` pro zajištění, že hodnota nemůže být negativní.

- **`__str__`**:
  - Poskytuje textovou reprezentaci počtu a typu OOP jako položky objednávky.

### Shrnutí modelů v aplikaci `calculator`:

Tyto modely slouží k vytvoření základního systému pro správu objednávek v rámci platformy, 
kde každý uživatel (`CustomUser`) může vytvářet objednávky (`CalculatorOutput`) obsahující jednu nebo více 
položek ochranných prostředků (OOP), které jsou konkrétně specifikovány v `CalculatorItem`. Systém je navržen tak, 
aby flexibilně podporoval revizi a úpravu objednávek, přičemž poskytuje přesné vedení účtování s ohledem na množství a 
typ použitých prostředků.



### `revision/models.py`

#### Model `MaterialType` 

- **`name`**: Typ materiálu (např. Harness, Ropes).

#### Model `Manufacturer`

- **`name`**: Jméno výrobce.
- **`material_type`**: Odkazuje na `MaterialType`.
- **`lifetime_use_months`**: Maximální doba používání.
- **`lifetime_manufacture_years`**: Maximální doba od data výroby.

#### Model `TypeOfPpe` 

- **`group_type_ppe`**: Identifikuje skupinu OOP (osobních ochranných prostředků).
- **`price`**: Cena asociovaná se skupinou PPE.
- **`__str__`**: Vrací textovou reprezentaci s názvem a cenou.

#### Model `RevisionData`

- **`image`**: Obrázek spojený s typem revize.
- **`manufacturer`**: Odkazuje na `Manufacturer`.
- **`group_type_ppe`**: Odkazuje na `TypeOfPpe`.
- **`name_ppe`**, **`standard_ppe`**: Název a standard ochranného prostředku.
- **`manual_for_revision`**: Manuál k revizi.

#### Model `RevisionRecord`

- **`revision_data`**: Odkazuje na `RevisionData`.
- **`serial_number`**: Unikátní sériové číslo.
- **`date_manufacture`, `date_of_first_use`**: Datum výroby a prvního použití.
- **`date_of_revision`, `date_of_next_revision`**: Datum poslední a příští revize.
- **`owner`**: Odkazuje na `CustomUser`.
- **`item_group`**: Přiřazeno k `ItemGroup`.
- **`verdict`**: Hodnocení stavu položky.
- **`notes`**: Poznámky.
- **`__str__`**: Textová reprezentace objektu.
