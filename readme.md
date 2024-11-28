zamyslet se nad pouzitim forms pro kalkulacku, 

# Projekt revize OOPP a Práce ve výškách

## Struktura webu 

### revision
- zde se budou vkladat revize oopp a manipulovat s mini 
- 
## Strukturovaný popis projektu a fáze vývoje
1. Kalkulačka ceny revize OOPP
- Funkce: Počítání ceny revize na základě počtu a typu položek, zohlednění formy dopravy (zákazníkova adresa / uživatelova adresa).
- Registrace: Po výpočtu se zákazníkům nabídne formulář pro registraci a odeslání poptávky.
- Backend integrace: Kalkulačka a registrace se propojí s backendem, kde se poptávka ukládá do databáze.
 2. Efektivní zpracování záznamů o revizi.
- Skenování QR kódů: Automatické nahrávání údajů z QR kódů do databáze.
- Automatizace protokolů: Export dokumentů s výsledky revize a přehledem položek.
- Upozornění na expiraci revizí: Systém upozorňuje zákazníky před vypršením platnosti revize a nabízí termíny k nové revizi.
3. Poptávky na optimalizaci pracovních postupů
- Formulář optimalizace: Obsahuje rozvinuté otázky, které pomáhají získat klíčové informace o potřebách zákazníka.
- Správa dat: Zpracování poptávek a přehled o konzultacích.
4. Fakturace
- Automatické faktury: Systém generuje faktury na základě poptávek a záznamů o provedené revizi.
 5. Kalendář s dostupnými termíny
- Interní správa: Vložíte objednávky a dostupné termíny ručně.
- Automatické rezervace: Zákazníci si mohou sami rezervovat volné termíny.


## Funkcionalita 
- [ ]  Kalkulačka ceny revize OOPP
    - [ ] Funkce: Počítání ceny revize na základě počtu a typu položek, zohlednění formy dopravy 
        (zákazníkova adresa / uživatelova adresa).
    - [ ] Registrace: Po výpočtu se zákazníkům nabídne formulář pro registraci a odeslání poptávky.
    - [ ] Backend integrace: Kalkulačka a registrace se propojí s backendem, kde se poptávka ukládá do databáze.


## Kalkulačka
- Příklad dat pro tabulku kalkulator:

| ID  | Druh OOPP                  | Cena (Kč) |
|-----|----------------------------|-----------|
| 1   | Karabina                  | 100       |
| 2   | Lano                      | 200       |
| 3   | Celotělový úvazek         | 500       |
| 4   | Arboristický úvazek       | 550       |
| 5   | Lezecký úvazek            | 450       |
| 6   | Helma                     | 150       |
| 7   | Arboristická helma        | 180       |
| 8   | Slaňovací brzda běžná     | 250       |
| 9   | Slaňovací brzda antipanic | 300       |
| 10  | Slaňovací brzda speciální | 350       |
| 11  | Tlumič pádu "I"           | 400       |
| 12  | Tlumič pádu "Y"           | 450       |
| 13  | Zachycovač pádu jednoduchý| 100       |
| 14  | Zachycovač pádu složitý   | 150       |
| 15  | Kladka                    | 200       |




kalkulator na frontendu upravit tak aby jsem nemusel vkladat data jak to index.html tak do tabulky v databazi. 

postup bych videl tak ze kalkulator bude mit ve sloupci polozka uvedeny odkaz a pokud budu nekdy menit nazvy zmenim je pouze na jednom miste a zmena se provede vsude. 

- [ ]
- [ ] zadavani počtu jednotlivich položek
    

## Poptávkový formulař



## Databáze 

### Modely 

- [ ] seznam druhů oopp
  - [ ] id - primární klíč, jedinečné ID pro každou položku ceny.
  - [ ] group_type_ppe - popis druhu OOPP (např. karabina, lano, celotělový úvazek, arboristický úvazek, helma, atd.).
  - [ ] cena - cena za revizi jednoho kusu daného druhu OOPP.
- [ ] hromadny_evidencni_list_oopp
  - [ ] id - primární klíč, jedinečné ID pro každou položku OOPP
    - [ ] firma_list_id - cizí klíč na tabulku firma_evidencni_listy, propojuje jednotlivé položky OOPP s konkrétním seznamem firmy
    - [ ] zakaznik_id - cizí klíč na tabulku zakaznici, umožňuje spojit jednotlivé položky OOPP s konkrétním zákazníkem
    - [x] name_ppe - název OOPP (např. lano, helma, apod.)
    - [ ] PPE category  - norma OOPP (např. EN 358, EN 361)
    - [ ] manufacturer - výrobce dané položky
    - [ ] serial_number - sériové číslo položky
    - [ ] date_manufakture - datum výroby položky
    - [ ] date_of_first_use - datum, kdy byla položka poprvé použita
    - [ ] date_of_revision - datum poslední revize
    - [ ] date_of_next_revision - datum příští revize
    - [ ] verdict - výsledek revize (např. "vyhovuje" nebo "nevyhovuje")
    - [ ] notes - další poznámky k revizi položky
- [ ] firma_list_id #TODO dořešit strukturu tabulky 
  - Firma vytvoří v systému různé seznamy OOPP pro svá pracoviště nebo jednotlivé zaměstnance.
  - Každá položka OOPP, která je přidána, se přiřadí k odpovídajícímu evidenčnímu listu (např. „Stavba A – pracovník Novák“).
  - Tím se zajistí, že každá firma může spravovat své OOPP dle svých interních struktur – podle pracovních míst nebo zaměstnanců.

- [ ]  firma_evidencni_listy
  - [ ] id - primární klíč, jedinečné ID pro každý seznam
  - [ ] firma_id - cizí klíč na tabulku zakaznici, identifikuje firmu, které evidenční list patří
  - [ ] nazev_listu - pojmenování seznamu (např. jméno zaměstnance nebo název pracoviště, např. „Stavba A – pracovník Novák“)
  - [ ] datum_vytvoreni - datum vytvoření tohoto evidenčního listu
  - [ ] popis - doplňkový popis, který přiblíží účel nebo podrobnosti evidenčního listu

- [ ] zakaznici 
  - [ ] id - primární klíč, jedinečné ID pro každého zákazníka
  - [ ] jmeno - jméno zákazníka
  - [ ] prijmeni - příjmení zákazníka
  - [ ] nazev_firmy - název firmy zákazníka
  - [ ] adresa - adresa zákazníka (s možností rozdělení na ulice, město, PSČ, pokud je potřeba)
- [ ] Revision
  - [ ] id - primární klíč, jedinečné ID pro každou revizi
  - [ ] druh_oopp - druh OOPP
  - [ ] vyrobce - výrobce položky
  - [ ] norma - norma revizního vybavení
  - [ ] manual_odkaz - odkaz na manuál, který obsahuje pokyny k provádění revize
  - [ ] zivotnost - maximální životnost položky od data výroby a prvního použití (např. „10 let od prvního použití, 15 let od výroby“)
  - [ ] Další funkcionalita: Bude propojená s tabulkou hromadny_evidencni_list_oopp prostřednictvím druhu a normy položky. Systém bude sledovat expiraci životnosti položky na základě data prvního použití a data výroby.



