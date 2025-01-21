# Dokumentace k řízení přístupových práv v projektu Django

## Úvod
Tento dokument popisuje strukturu a požadavky pro řízení přístupových práv uživatelů ve webové aplikaci postavené na Django. Cílem je definovat, co jednotliví uživatelé mohou vidět a dělat v aplikaci na základě jejich role. Tato pravidla jsou důležitá pro zajištění bezpečnosti, soukromí a organizační struktury celé aplikace.

## Role uživatelů

### Admin
- [ ] Vidí a má přístup ke všem částem aplikace.
- [ ] Má práva na úpravy, mazání a spravování jakýchkoli dat v aplikaci.

### Revision Technician
- [ ] Vidí všechny registrované uživatele a firmy.
- [ ] Má přístup ke všem záznamům v aplikaci `revisions`.
- [ ] Má omezená práva na mazání a úpravy v aplikaci `revisions`.

### Company Supervisor
- [ ] Vidí všechny záznamy v `revisionRecord`, ale pouze ty, které patří k jeho firmě.
- [ ] Je označen jako owner pro `revisionRecord`.
- [ ] Nemůže mazat ani editovat v app `revisions`, pouze prohlížení.
- [ ] Vidí všechny zaměstnance ve firmě v aplikaci `accounts`.
- [ ] Může měnit informace pro svoji firmu ve `Company View` pomocí Edit.
- [ ] Může editovat jednotlivé zaměstnance.
- [ ] Může přidávat `ItemGroup` pro svoji firmu, nově vytvořené `ItemGroup` jsou automaticky přiřazeny jeho firmě.
- [ ] Může upravovat `ItemGroup`, kterých je vlastníkem.
- [ ] Může upravovat `revisionRecord` a to pridanim forky, zapisem `retire` + v budoucnu pridat komentář s 
      mimořádné události (pád z větší výšky, poškození, drobné závady)
- [ ] Může přidávat nový výrobek `revisionRecord` s nastavením na `NEW` a datem přidání jako `first_use` pri tomto 
      zapisu je vyzadovana fotka polozky a nastaven `checked_record=False`


### Company User
#### app accounts
- [ ] Vidí svůj profil a může jej upravovat
- [ ] Vidí svoji firmu, ale nemůže ji upravovat.
- [ ] Vidí `ItemGroup`, které patří jeho firmě.
- [ ] Může upravovat pozici jednotlivých `revisionRecord` v `ItemGroup`, kde je jako `user`.
- [ ] Může vyjmout záznam z `ItemGroup` a přesunout ho do `free_revision_records`.
- [ ] Může přidat záznam z `free_revision_records` do své `ItemGroup`.
- [ ] Může přidat komentář (`Content Type`) ohledne mimořádných událostí ohledne jednotlivich položek součástí může být i fotka
#### app Revisions
- [ ] Vidi všechny zaznamy a `revisionrecords` sve firmy ve kterych muze pouze hledat a koukat na detaily.
- [ ] nemuze zde editovat ani mazat. 

### SafetyCheck
- prava pro Bezpečnostní kontrolu prováděnou při výkonu práce oprávněnou osobou pro kontrolu `RevisionRecords` jednotlivich `CustomUser`
- tato osoba dostane pomoci `QR codu` pristup k `RevisionRecord` kontrolovaného `CustomUser` ktery ve své strance požádá a vigeneruje `QR cod` pro pristup k funkcionalite (API)
kde bude jednoduse moci spontrolovat všechny zaznamy tohoto uživatele a udělat zapis o provedení teto kontroly a exportovat si data. 
- Přístup pouze k zaznamum určitého `CustomUser`/`Company` a jejich `ItemGroup`

## Implementace práv v Django

### Postup
1. **Použití Django groups**: Rozdělte role uživatelů pomocí Group modelu v Django a přidělte jim konkrétní práva.
   
2. **Custom permissions**: Vytvořte vlastní příznaky oprávnění (permissions) pro specifické akce, které jednotliví uživatelé mohou vykonávat.

3. **Role-based Access Control (RBAC)**: Použití RBAC pro definování rolí a přístupových práv, což je flexibilní a snadno rozšiřitelné řešení.

4. **Smart QuerySets a views**: Přizpůsobte dotazy a views pro filtrování výsledků, aby uživatelé viděli pouze to, na co mají právo (např. `ItemGroup` spojené s jejich firmou).

5. **Formulářová logika**: Využijte Django formuláře (Forms) k omezení viditelnosti a úprav u položek, jako jsou `ForeignKey` pole, na základě uživatelských rolí.

6. **Custom middleware**: Přidejte middleware pro kontrolu specifických access violations a logging.

7. **Unit Testing**: Implementujte jednotkové testy pro zajištění správného chování oprávnění.

## Konečné doporučení
- Vyhněte se příliš složité manuální logice v každém view a modelu. Místo toho se zaměřte na konfiguraci oprávnění na úrovni modelů a prostřednictvím Django's built-in mechanisms (jako jsou Groups a Permissions).
- Udržujte oprávnění jednoduchá a dobře dokumentovaná. Rozhodněte se, kde budete řešit oprávnění - zda na úrovni modelů, views nebo v šablonách, a snažte se tuto volbu udržet konzistentní skrz celou aplikaci.
- Přemýšlejte o použití open-source knihoven pro řízení přístupu a oprávnění, které jsou často velmi užitečné a mohou ušetřit čas.

Doporučené knihovny a zdroje pro hlubší studium:
- [Django Guardian](https://django-guardian.readthedocs.io/en/stable/) pro object-level permissions.
- [Django REST Framework](https://www.django-rest-framework.org/) pro API zabezpečení a oprávnění.