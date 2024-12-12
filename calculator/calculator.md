#### Backend - Zobrazení Formuláře

1. **Příprava dat pro zobrazení formuláře**: Vytvořte pohled, který načte všechny položky a předá je do šablony.

```python
from django.shortcuts import render
from .models import TypeOfPpe

def calculator_view(request):
    ppes = TypeOfPpe.objects.all()
    return render(request, 'calculator.html', {'ppes': ppes})
```
#### Front-end - HTML a JavaScript

2. **Formulář a uložený stav**: V HTML šabloně načtěte data pomocí kontextu a použijte JavaScript pro uložení a načtení stavu z `localStorage`.
### Jak to funguje

- **Backend**: Pohled `calculator_view` načte všechny položky z databáze a předá je šabloně pro formulář.

- **Frontend**: JavaScript zajišťuje uložení stavu zadaného uživatelem. Když se count pro každou položku změní, okamžitě se uloží do `localStorage`.

- **Obnovení stavu**: Při načtení stránky používá JavaScript data z `localStorage` k obnovení formuláře do stavu, ve kterém byl naposledy.

Tento přístup minimalizuje složitost a využívá silných stránek obou, backendu a frontendových řešení, k poskytnutí vyrovnaného a uživatelsky přívětivého zážitku.



```python
 def calculate_total(self):
        """
        Metoda pro výpočet celkové ceny na základě množství jednotlivých položek a volitelných nákladů.
        Předpokládejme, že máte funkce na získání cen podle TypeOfPpe.
        """
        # Jestliže máte další tabulku pro ceny, můžete je přímo vyhledávat a počítat
        self.total_price = (
            self.karabina_count * 100 +
            self.lano_count * 3 +
            self.celotelovy_uvazek_count * 500 +
            self.arboristicky_uvazek_count * 550
            # Přidejte další výpočty podle položek...
        )

        if self.revize_u_zakaznika:
            self.total_price += self.cesta_km * 10 + 500  # předpokládám základní poplatek 500 Kč
        if self.prepravni_sluzba:
            self.total_price += 200
        # osobní předání nemá náklady

        self.save()

    def __str__(self):
        return f"Order by {self.customer} on {self.created_at}: {self.total_price} Kč"

```

### Vysvětlení

- `customer`: Odkaz na uživatele, který zadal objednávku pro vazbu na model uživatele (například `CustomUser`).

- `created_at` a `updated_at`: Automatické pole pro sledování, kdy byla objednávka vytvořena a naposledy aktualizována.

- `total_price`: Decimal pole k uchování vypočítané celkové ceny objednávky.

- `calculate_total`: Metoda, která na základě aktuálních počtů a volitelných položek přepočítá celkovou cenu.

Pamatujte, že budete muset implementovat logiku pro výpočet cen dle aktuálních cen v tabulce `TypeOfPpe`, abyste udržovali přesnost v případě změn cen.

### Jak to funguje:

- **`TypeOfPpe`**: Definuje dostupné typy OOPP a jejich ceny.
- **`CalculatorOutput`**: Obsahuje základní informace o objednávce a odkazuje na zákazníka.
- **`CalculatorItem`**: Ukládá informace o každé položce v objednávce a množství jednotlivého typu OOPP.

### Výhody tohoto přístupu:

- **Modularita**: Můžete snadno přidávat nové typy OOPP bez změny struktury `CalculatorOutput`.
- **Flexibilita**: Měnit ceny OOPP bez nutnosti úprav kódu.
- **Udržovatelnost**: Snadné rozšíření a údržba systému.

#### `CalculatorOrder`

- Obsahuje odkazy na uživatele (zákazníka) a sledování stavu objednávky.
- Poskytuje prostředky pro výpočet celkové ceny revize.
- Používá metody `__str__` a `__repr__` pro čitelnou a podrobnou reprezentaci.

#### `CalculatorItem`

- Modeluje jednotlivé položky v rámci objednávky `CalculatorOrder`.
- Umožňuje uživatelům zadat množství pro každý typ položky, přičemž používá `MinValueValidator` pro zajištění, že množství je logické.

### Závěrečné úvahy:

- **Validace dat**: Zajistěte, že všechen váš logický kód pro výpočet ceny a zpracování objednávek je testován.
- **Migration Mějte jistotu, že veškeré změny, které jste provedli v modelech, jsou správně reflektovány v migracích (pomocí `python manage.py makemigrations` a `python manage.py migrate`).
    helmets = IntegerField(default=0)
    arborist_helmets = IntegerField(default=0)
    fall_arrest_harness = IntegerField(default=0)
    height_work_harness = IntegerField(default=0)
    arborist_harness = IntegerField(default=0)
    chest_harness = IntegerField(default=0)
    seat_harness = IntegerField(default=0)
    rescue_equipments = IntegerField(default=0)
    descenders = IntegerField(default=0)
    arborist_descenders = IntegerField(default=0)
    asaps = IntegerField(default=0)
    fall_arrests = IntegerField(default=0)
    ascenders = IntegerField(default=0)
    pulleys = IntegerField(default=0)
    block_pulleys = IntegerField(default=0)
    special_pulleys = IntegerField(default=0)
    carbines = IntegerField(default=0)
    slings = IntegerField(default=0)
    steel_lanyard = IntegerField(default=0)
    positioning_lanyards = IntegerField(default=0)
    fall_absorbers = IntegerField(default=0)
    fall_absorbers_with_conectors = IntegerField(default=0)
    cambium_savers = IntegerField(default=0)
    cambium_savers_special = IntegerField(default=0)
    rigging_plate = IntegerField(default=0)
    rope = IntegerField(default=0)
    rope_spliced_eye = IntegerField(default=0)

**atributy kalkulačky**
- Příklad dat pro tabulku kalkulator:

| **id** | **TypeOfPpe**               | **price** | **ks** |
|--------|----------------------------|-----------|-------|
| 1      | helmets                     | 1000 CZK  | 0     |
| 2      | arborist_helmets            | 1200 CZK  |       |
| 3      | fall_arrest_harness         | 1500 CZK  | 15    |
| 4      | height_work_harness         | 1800 CZK  | 7     |
| 5      | arborist_harness            | 2000 CZK  | 5     |
| 6      | chest_harness               | 1100 CZK  | 12    |
| 7      | seat_harness                | 1300 CZK  | 10    |
| 8      | rescue_equipments           | 5000 CZK  | 3     |
| 9      | descenders                  | 900 CZK   | 20    |
| 10     | arborist_descenders         | 1200 CZK  | 6     |
| 11     | asaps                       | 2500 CZK  | 5     |
| 12     | fall_arrests                | 3000 CZK  | 4     |
| 13     | ascenders                   | 1100 CZK  | 10    |
| 14     | pulleys                     | 800 CZK   | 25    |
| 15     | block_pulleys               | 950 CZK   | 20    |
| 16     | special_pulleys             | 1500 CZK  | 8     |
| 17     | carbines                    | 300 CZK   | 50    |
| 18     | slings                      | 600 CZK   | 30    |
| 19     | steel_lanyard               | 1800 CZK  | 10    |
| 20     | positioning_lanyards        | 1400 CZK  | 12    |
| 21     | fall_absorbers              | 2200 CZK  | 8     |
| 22     | fall_absorbers_with_conectors | 2500 CZK | 5     |
| 23     | cambium_savers              | 1900 CZK  | 7     |
| 24     | cambium_savers_special      | 2500 CZK  | 4     |
| 25     | rigging plate               | 1300 CZK  | 15    |
| 26     | rope                        | 2500 CZK  | 20    |
| 27     | rope_spliced_eye            | 3500 CZK  | 3     |



### Shrnutí

- **Dynamická generace formulářů**: Vytvořte dynamická pole pro všechny položky.
- **Validace a zpracování formulářových dat**: Zajistěte, že `quantity` bude vždy alespoň 0 a proveďte výpočty na serverové straně.
- **Interaktivní šablona**: Použijte šablony Django k efektivnímu vykreslení tabulky a formuláře.
