### `clean` Metody ve Forms

1. **Umístění v `forms.py`**: Metody pro čištění dat (`clean_<fieldname>` nebo obecné `clean`) by měly být umístěny ve třídách formulářů v souboru `forms.py`. Tyto metody ti umožní validovat data při odeslání formuláře před uložením do databáze.

2. **Specifické metody `clean_<fieldname>`**: 
   - Slouží k validaci konkrétního pole. Například, pokud chceš validovat unikátnost nebo formát určitého pole.
   - Výsledná chybová zpráva by se měla objevit přímo u tohoto pole ve formuláři.

3. **Obecná metoda `clean`**:
   - Použij k validaci celého formuláře nebo pro závislé validace mezi různými poli.
   - Například, pokud určité pole závisí na jiné hodnotě, můžeš to zkontrolovat zde.

### Zobrazení Chybových Hlášek

1. **Připojení chyb k příslušným polím**:
   - Django automaticky přidává chybové zprávy k příslušným polím ve formuláři, když použiješ `form.add_error('fieldname', 'Chyba zprávy')`. Chyby definované v `clean_<fieldname>` jsou zobrazeny automaticky u příslušného pole.

2. **Zobrazení obecné chyby**:
   - Chcete-li obecnou chybu zobrazit v horní části formuláře, přidejte ji k `non_field_errors` pomocí: `self.add_error(None, 'Obecná chyba')`.

3. **Hlásky z `UniqueConstraint` nebo Databáze**:
   - Zprávy z úrovně databáze jsou často připojeny k non-field errors nebo přiřazeny specifickým polím, pokud to Django umí rozpoznat.