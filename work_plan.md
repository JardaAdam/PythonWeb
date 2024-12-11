zamyslet se nad pouzitim forms pro kalkulacku 

# Projekt revize OOPP a Práce ve výškách

## Web structure

### app Revision
- zde se budou vkladat revize oopp a manipulovat s mini 
- Formulář pro poptání revize ktery spocita cenu za revizi. Uživatel vloží do formuláře počty jednostlivých 
položek a fotmulař mu spočítá cenu.

## Strukturovaný popis projektu a fáze vývoje
1. Vytvoření databáze tabulek:
    - Profile = rozšiřující uživatele (adresa, telefon, email)
    - TypeOfPpe = název skupin, ceny jednotlivých skupin PPE
    - SheetOfPpe = seznam všech revidovaných položek
    - Revision = pomocna jsou zde všechny vyráběné položky a jejich návody na provedení revize
    - Inquiries = výstup z kalkulatoru 
2. Kalkulačka ceny revize OOPP ( Formulář )
**použité tabulky** -> TypeOfPpe
- **Funkce:**
  - [ ] Počítání ceny revize na základě počtu a typu položek
    - [ ] ošetření platnosti formuláře při delší době vyplnování nesmí
    zákazník přijít o vyplněná data
  - [ ] Počítání nákladů na dopravu
    - [ ] revize u zákazníka (sídlo revizního technika -> zákazníkova adresa).
    - [ ] revize u revizního technika
      - [ ] osobní předání 
      - [ ] přepravní společnost
- [ ] spočítání ceny revize
  - [ ] tlačítko spočítat cenu revize
    - [ ] zobrazí výslednou cenu revize a uloží zadané informace -> Table Inquiries
    - [ ] pokud zákazník má zájem o revizi odesle poptávkoví formulář
      - [ ] registrovaný 
        - [ ] cena revize i s dopravou
        - [ ] odešle poptávku na email 
          - [ ] informace o velikosti zakázky
          - [ ] deadline 
      - [ ] neregistrovaný 
        - [ ] ukládání informaci o zakázce
          - před odesláním formuláře kolonka email -> pro identifikaci zakazníka 
        - [ ] cena revize bez dopravy 
        - [ ] nabídka registrace



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


| id | Další volitelné položky  | Cena                    | ks |
|----|--------------------------|-------------------------|---|
| 16 | Revize u zákazníka cesta | 10kč/km<br/>Praha=500kč |   |
| 17 | Přepravní služba         | 200 kč                  |   |
| 18 | Osobní předání Úvaly     | 0 kč                    |   |
| 19 | Celková cena za revizi   | spocitaná cena          |---|

3. Provádění revizí
**použité tabulky** -> SheetOfPpe, Profile, Revision
- [ ] přiřazení revize k uživateli -> **Table = Profile** 
  - [ ] dělení do skupin 
    - [ ] uživatel (firma) může pod jednou registrací mít více skupin -> CompanyLists ( batohů, zaměstnanců, ...)
- [ ] **zadávání** jednotlivých položek do databáze
  - [ ] **Teble revizion** poskytuje našeptávání položek podle **name_ppe**
    - [ ] vyplnuje sloupce -> standart_ppe, manufakturer
    - [ ] hlídá životnost dle -> lifetime_use, lifetime_manufacture
    - [ ] automaticky vyplnuje -> date_of_revision (actual date), date_of_next_revision ( 12 month)
      - [ ] hlídá datum další revize a (měsíc) před koncem revize posílá notifikaci zákazníkovy
  - [ ] Skenování QR kódů, skenovaní textu: skenování -> serial number, QR kodu na výrobku
    - [ ] vyhledávání položky podle **serial_number** ( opakovaná revize )
- [ ] **Export** dokumentů s výsledky revize a přehledem položek 
  - [ ] hlavička dokumentu
    - [ ] uživatel -> Profile
    - [ ] podskupina uživatele -> Profile - group of items
    - [ ] udaje o reviznim technikovy
  - [ ] tabulka dokumentu -> name_ppe, standart_ppe, manufacturer, serial_number, date_of_manufacture, date_of_first_use, 
  date_of_revision, date_of_next_revision, verdict, notes
- [ ] **Upozornění**  
  - [ ] expiraci revizí: Systém upozorňuje zákazníky před vypršením platnosti revize a nabízí termíny k nové revizi.
  - [ ] stažení výrobku ( položky ) z trhu a další upozornění výrobce 
    - [ ] informování uživatele emailem 
    - [ ] označení položky v **SheetOfPpe** při otevření uživatelem nebo revizním technikem
      - [ ] oznámení od výrobce se uloží do **Revision** column warning 
-
4. **zadávání dat uživatelem**
- [ ] registrovaný uživatel s vytvořenou revizí si při koupi nové položky
  - [ ] zvolí v **CompanyLists** kam položku přidá
  - [ ] zapíše položku do své **SheetOfPpe** s atributi
    - [ ] group_type_ppe
    - [ ] name_ppe
    - [ ] manufacturer
    - [ ] serial_number
    - [ ] date_of_manufacture
    - [ ] date_of_first_use
    - [ ] verdict -> defaultne NEW 
5. **Fakturace**
- Automatické faktury: Systém generuje faktury na základě poptávek a záznamů o provedené revizi.
6. Kalendář s dostupnými termíny
- Interní správa: Vložíte objednávky a dostupné termíny ručně.
- Automatické rezervace: Zákazníci si mohou sami rezervovat volné termíny.






- [ ] **Formulář** ve kterém uživatel zadá počet jednotlivých položek u každé **group_type_ppe** bude klikací 
  odkaz na výčet jednotlivých **name_ppe** aby uživatel správně zařadil položku 
  - [ ] formulář musí být chráněný proti bezpečnostnímu limitu odeslání tak abz mohl uživatel vzplnovat jak dlouho chce 
  a nestalo se že v půlce vyplnování nbo na konci vyplnění kdz chce formulář odeslat přijde o data
  - [ ] propojení s **Models** 
    - [ ] TypeOfPpe -> údaje o cene
    - [ ] Revision -> proklikávací odkaz co spadá do této **group_type_ppe**
    - [ ] User -> adresa pro výpočet cesty k zákazníkovy
    - [ ] po zadání všech položek a kliknutí na spočítat se ukáže uživately celková částka za revizi a nabídne se mu 
    odeslat objednávku na revizi -> **Button odeslat** odešle informace uživatelem zadaných počtech a zvoleném způsobu revize 
    na email Admin ( rezervace@revizeOOPP.cz)

kalkulator na frontendu upravit tak aby jsem nemusel vkladat data jak to index.html tak do tabulky v databazi. 

postup bych videl tak ze kalkulator bude mit ve sloupci polozka uvedeny odkaz a pokud budu nekdy menit nazvy zmenim 
je pouze na jednom miste a zmena se provede vsude. 

- [ ]
- [ ] zadavani počtu jednotlivich položek
    

# Poptávkový formulař



# Databáze 

## Models

- [x] **User** 
  - [x] user_name - (CharField)
  - [x] first_name - (CharField)
  - [x] last_name - (CharField)
  - [x] email - (EmailField)
  - [x] password - (CharField)
  - [x] is_active (BooleanField): Určuje, zda je účet aktivní (např. deaktivovaný uživatel nebude mít přístup).
  - [x] last_login (DateTimeField): Datum a čas posledního přihlášení uživatele.
  - [x] date_joined (DateTimeField): Datum a čas vytvoření uživatelského účtu.
### accounts
- [x] **CustomUser**
  - [x] company_name
  - [x] adress
  - [x] city
  - [x] phone
  - [x] IČO
  - [x] DIC
  - [?] sheet_name (ProfileItemList)
  - [x] discount ( sleva uzivatele )

### config
#### revisions

- [ ]  **ProfileItemList** spojovaci tabulka
  - [x] Profile - cizí klíč na tabulku zakaznici, identifikuje firmu, které evidenční list patří
  - [x] sheet_name - pojmenování seznamu (např. jméno zaměstnance nebo název pracoviště, např. „Stavba A – pracovník Novák“)
  - [x] create - datum vytvoření tohoto evidenčního listu
  - [x] update - datum provedení změn
  - [x] information - doplňkový popis, který přiblíží účel nebo podrobnosti evidenčního listu

- [ ] **Manufacturer**
  - [ ] name = name of manufacturer of PPE

- [ ] **Expiration**
  - [x] manufacturer - ForeinKey 
  - [x] material - 
  - [x] lifetime_use - 
  - [x] lifetime_manufacture - 

- [ ] **TypeOfPpe**
  - [x] group_type_ppe - popis druhu OOPP (např. karabina, lano, celotělový úvazek, arboristický úvazek, helma, atd.).
  - [x] price - cena za revizi jednoho kusu daného druhu OOPP.
  - [ ] spojení této tabulky tak aby se zákazník mohl podívat co do této skupiny spadá



- [ ] **CalculatorOutPut**
- uklada data vkladana do formulare ktery pocita cenu za revizi. 
- varianta pro
    - nepřihlášeného uživatele -> použití `localStorage` v prohlížeči uživatele pomocí JavaScriptu
    - přihlášeného uživatele -> CustomUser


- [ ] **Revision**
  - [x] image - obrazek položky
  - [x] name_ppe - type OOPP (Tripel Lock, Expert  III, Adjust)
  - [x] manufacturer - výrobce položky
  - [?] material - bude stacit kdyz si to bude pamatovat podle vyrobce? 
  od výroby/od 1.použití Postroje-10/15,Textilní OOPP-10/15, Lana10/15, Kovové OOPP-neomezeně, Přilby-10
  - [x] manual_for_revision - odkaz na manuál, který obsahuje pokyny k provádění revize
  - [?] lifetime_use - maximální životnost položky od prvního použití (např. 10 let od prvního použití)
  - [?] lifetime_manufacture - maximální životnost položky od data výroby (např. 15 let od výroby“)
  - [?] warning - webscraping prefix notifikace výrobce o vadách a stahování z trhu
    - [ ] pokud bude součástí notifikace např. šarže zohlední se to i v upozornění pouze dotčených položek
    nebude se informovat plošně celí výrobek 
  - [ ] expiration bude propojená s tabulkou **SheetOfPpe** prostřednictvím **name_ppe** a **manufacturer**. 
  Systém bude sledovat expiraci životnosti položky na základě data prvního použití a data výroby. 


- [ ] **SheetOfPpe**
  - [?] company_lists - ForeignKey na tabulku firma_evidencni_listy, propojuje jednotlivé položky OOPP s konkrétním seznamem firmy
  - [ ] CustomUser - ForeignKey  na tabulku zakaznici, umožňuje spojit jednotlivé položky OOPP s konkrétním zákazníkem
  - [ ] group_type_ppe - ForeignKey popis druhu OOPP (např. karabina, lano, celotělový úvazek, arboristický úvazek, helma, atd.).
  - [ ] name_ppe - ForeignKey Type OOPP (Tripel Lock, Expert  III, Adjust)
  - [ ] manufacturer - ForeignKey výrobce dané položky
  - [ ] serial_number - sériové číslo položky
  - [ ] date_manufakture - datum výroby položky
  - [ ] date_of_first_use - datum, kdy byla položka poprvé použita
  - [ ] date_of_revision -datefield datum poslední revize
  - [ ] date_of_next_revision -datefield datum příští revize
  - [ ] verdict - výsledek revize anum(např. "vyhovuje" nebo "nevyhovuje")
  - [ ] notes -chrfield další poznámky k revizi položky




  



## Rope access work
- část webu kde nabízím práci ve výškách 
- Formulář pro yadání poptávky
 
## 
- [ ] **Formulář optimalizace**
  - [ ] Obsahuje rozvinuté otázky, které pomáhají získat klíčové informace o potřebách zákazníka.
- [ ] Správa dat: Zpracování poptávek a přehled o konzultacích.
