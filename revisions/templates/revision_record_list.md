### Dokumentace k šabloně: `revision_record_list.html`

#### Struktura Šablony

1. **Rozšíření základní šablony**:
   - Šablona začíná příkazem `{% extends 'revision_base.html' %}`, což znamená, že využívá společné rozvržení a styly 
   definované v základní šabloně `revision_base.html`.

2. **Blok pro nadpis stránky**:
   - Blok `{% block title %}` určuje, jaký bude nadpis stránky při zobrazení v prohlížeči. Zde je to nastaveno na 
   hodnotu "Revision Records".

3. **Hlavní Obsah Stránky (`revision_content`)**:
   - Blok `{% block revision_content %}` obsahuje hlavní část obsahu stránky, včetně logiky interakce a tabulky záznamů.

#### Hlavní Komponenty

1. **Nástroje na úpravu obsahu**:
   - Na začátku obsahu je tlačítko "Add Revision Record", které umožňuje přidat nový záznam. Tlačítko odkazuje na 
   view `add_revision_record`.

2. **Formulář pro vyhledávání**:
   - HTML formulář pro vyhledávání obsahuje textové pole a tlačítko pro odeslání GET požadavku. Výsledky hledání se 
   upraví na základě přítomného textu v poli.

3. **Tabulka zobrazující záznamy**:
   - Obsahuje hlavičky sloupců, které se používají k řazení záznamů, a nabízí uživateli možnost řazení 
   záznamů podle daného sloupce kliknutím.
   
4. **Interaktivní hlavičky sloupců**:
   - Každá hlavička obsahuje odkaz, který při volbě přidá (nebo změní) parametry `sort_by` a `sort_order` v URL. 
   Tyto parametry jsou kontrolovány pomocí `{% if %}` směrnice, která určuje aktuální stav řazení a mění ho.

5. **Tělo Tabulky**:
   - Prostřednictvím smyčky `{% for record in revision_records %}` se zobrazuje každý záznam na řádku tabulky. 
   K dispozici je několik atributů záznamů, jako například výrobce, typ skupiny, datum revize, a další.

6. **Duplikovaný záznamový řádek**:
   - Pokud nejsou k dispozici žádné záznamy, šablona použije uvnitř `{% empty %}` hlášku, která informuje uživatele, 
   že nebyly nalezeny žádné záznamy.

7. **Akční Odkazy pro každý Záznam**:
   - Na konci řádku každého záznamu jsou k dispozici tři odkazy (prohlížení detailů, úprava, odstranění), které vedou na 
   příslušné pohledy definované pomocí URL názvů.

#### Celkový Přehled

Šablona `revision_record_list.html` poskytuje ucelený pohled na záznamy revizí, se zaměřením na funkčnost aktivního 
řazení a vyhledávání. Každý element je navržen tak, aby mohl být dynamicky ovládán pomocí GET parametrů URL, což dělá 
tento systém flexibilním a uživatelsky přívětivým. Doporučuje se zajistit, že související URL pravidla a naučené 
procesy frameworku Django jsou správně implementovány v rámci tvé aplikace, aby byly zajištěny náležité funkce a navigace.