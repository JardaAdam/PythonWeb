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