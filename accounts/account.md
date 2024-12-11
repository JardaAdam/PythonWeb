### Model `Country`

- **`name`**: Uchovává název země jako unikátní identifikátor, což umožňuje jeho používání jako klíč k přiřazování formátů a předpon.
- **`business_id_format`**: Ukládá regulární výraz určený pro validaci formátů obchodních identifikátorů (například IČO) pro danou zemi.
- **`tax_id_format`**: Ukládá regulární výraz pro validaci formátů daňových identifikátorů pro danou zemi.
- **`tax_id_prefix`**: Uchovává přednastavený prefix pro `tax_id`, například "CZ" pro Českou republiku.
- **`phone_number_prefix`**: Ukládá standardní předvolbu (prefix) pro telefonní čísla v rámci dané země.
- **`postcode_format`**: Ukládá regulární výraz k validaci poštovních směrovacích čísel pro konkrétní zemi.

### Model `CustomUser`

- **Dědění z `AbstractUser`**: Využívá zabudovaných vlastností a funkcionalit Django uživatelského modelu s rozšířením pro přidání specifických potřeb.
- **`company_name`, `address`, `city`**: Uložení doplňkových informací o uživateli spojených s firmou a umístěním.
- **`country`**: Reference na model `Country`, která umožňuje přizpůsobení formátů dat podle zvolené země.
- **`business_id`, `tax_id`**: Uložení identifikačních čísel společnosti, s validací a úpravou předvyplněných hodnot podle zvoleného státu.
- **`postcode`**: Uložení a validace poštovního směrovacího čísla zadaného uživatelem podle pravidel zvoleného státu.
- **`phone_number`**: Automatické nastavení a validace telefonního čísla uživatele, doplněné standardní státní předvolbou.
- **`discount`**: Uložení procentuální slevy, která může být uživateli přidělena, s validací zavedenou pro zajištění správného formátu.
- **`can_view_multiple_groups`**: Boolean hodnota, která určuje, zda uživatel má přístup k více skupinám dat nebo pouze ke svým vlastním.
- **Meta a Přístupové metody**:
  - **`ordering`**: Určuje výchozí řazení podle uživatelského jména.
  - **`clean()`**: Validace vstupů pro uživatelské pole na základě specifik zemí, které jsou konfigurovány přes model `Country`.
  - **`__repr__` a `__str__`**: Umožňují snadnější a přehledné zobrazení uživatelských dat při volání metod pro debugování nebo vykreslování.

### Model `ItemGroup`

- **`name`**: 
  - Ukládá název skupiny položek jako textový řetězec s maximální délkou 64 znaků.
  - Slouží jako identifikátor pro každou skupinu, což pomáhá s její kategorizací a správou.

- **`user`**: 
  - Odkazuje na model `CustomUser` jako cizí klíč (ForeignKey).
  - Identifikuje vlastníka (`CustomUser`) skupiny položek, což umožňuje každému uživateli mít několik skupin.
  - Použití `on_delete=models.CASCADE` zajišťuje, že pokud je uživatel odstraněn, všechny jeho skupiny budou rovněž odstraněny.

- **`items`**: 
  - Definován jako `ManyToManyField` odkazující na `RevisionRecord`.
  - Umožňuje, aby každá skupina obsahovala více položek (`RevisionRecord`), a každá položka mohla být ve více skupinách, což podporuje flexibilní asociace.
  - `blank=True` umožňuje, aby skupina mohla být vytvořena bez předchozího přiřazení konkrétních položek.

### Klíčové vlastnosti

- **Integrace s modelem `Country`**: Přiřazení zemi umožňuje přístup k přizpůsobení každého atributu pro uživatelské zadávání dat.
- **Flexibilní validace**: Všechny reg-ex validátory mohou být nastavovány přímo v `Country`, čímž je usnadněno upravení pravidel bez úprav modelu `CustomUser`.
- **Automatické doplnění preddefinovaných hodnot**: Například předvolby `phone_number` zajišťují, že se telefonní čísla automaticky začínají na správnou předvolbu.


