### Dokumentace k šabloně: `revision_record_list.html`

#### Struktura Šablony

1. **Rozšíření základní šablony**:
   - Šablona začíná příkazem `{% extends 'revision_base.html' %}`, což znamená, že využívá společné rozvržení a styly 
   definované v základní šabloně `revision_base.html`.

2. **Načtení templatetagu pro řazení**:
   - Příkaz `{% load sort_tags %}` se stará o načtení vlastní knihovny templatetagů, která zahrnuje `sort_link` 
   pro použití v šabloně.

3. **Blok pro nadpis stránky**:
   - Blok `{% block title %}` určuje, jaký bude nadpis stránky při zobrazení v prohlížeči. 
   Zde je to nastaveno na hodnotu "Revision Records".

4. **Hlavní Obsah Stránky (`revision_content`)**:
   - Blok `{% block revision_content %}` obsahuje hlavní část obsahu stránky, včetně logiky interakce a tabulky záznamů.

#### Hlavní Komponenty

1. **Nástroje na úpravu obsahu**:
   - Na začátku obsahu je tlačítko "Add Revision Record", které umožňuje přidat nový záznam. 
   Tlačítko odkazuje na view `add_revision_record`.

2. **Formulář pro vyhledávání**:
   - HTML formulář pro vyhledávání obsahuje textové pole a tlačítko pro odeslání GET požadavku, 
   což upraví výsledky hledání na základě přítomného textu.

3. **Tabulka zobrazující záznamy**:
   - Obsahuje hlavičky sloupců, které se používají k řazení záznamů, a nabízí uživateli možnost řazení záznamů 
   podle daného sloupce kliknutím.

4. **Interaktivní hlavičky sloupců**:
   - Použití templatetagu `{% sort_link %}` z knihovny `sort_tags` zajišťuje dynamické generování odkazů pro řazení. 
   Tento tag automaticky upraví parametry `sort_by` a `sort_order` v URL na základě aktuálního stavu řazení a změní ho.

5. **Tělo Tabulky**:
   - Prostřednictvím smyčky `{% for record in revision_records %}` se zobrazuje každý záznam na řádku tabulky. 
   K dispozici je několik atributů záznamů, jako například výrobce, typ skupiny, datum revize, a další.

6. **Zpráva pro prázdnou tabulku**:
   - Pokud nejsou k dispozici žádné záznamy, šablona zobrazí zprávu uvnitř `{% empty %}` bloku, 
   která informuje uživatele, že nebyly nalezeny žádné záznamy.

7. **Akční Odkazy pro každý Záznam**:
   - Na konci řádku každého záznamu jsou k dispozici tři odkazy (prohlížení detailů, úprava, odstranění), 
   které vedou na příslušné pohledy definované pomocí URL názvů.

#### Celkový Přehled

Šablona `revision_record_list.html` poskytuje ucelený pohled na záznamy revizí, se zaměřením na funkčnost 
aktivního řazení a vyhledávání. Použití templatetagu `sort_link` zajišťuje čistou a konzistentní logiku řazení, 
což dělá tento systém flexibilním a uživatelsky přívětivým. Doporučuje se zajistit, že související URL pravidla a 
procesy v rámci frameworku Django jsou správně implementovány, aby byly zajištěny náležité funkce a navigace.