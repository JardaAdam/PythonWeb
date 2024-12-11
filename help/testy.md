## Postup
- napsat testy hned po tom co napisu funkcionalitu !!
- testy napisu vzdy v aktualni branch a pak se merguje spolecne s kodem do Dev
- testy delame v kazde branche -> kazde aplikaci (viewer)
- muzeme vytvaret i vlastni testovaci soubory -> nazev by mel zacitan test*.py
  - pokud je testu hodne je vhodne udelat vice souboru -> delit pro lepsi prehlednost
- viewer/tests.py 
  - 

## Spousteni testu 
- sputsi vsechny testy v souborech zacinajici na slovo test
```python
python manage.py test
```
spousteni urciteho souboru s testy 
```python
python manage.py test viewer.test_models
```
- Zakladni testy se spousteji na vyrtualni databazy ktera je prazdna ale obsahuje stejne tabulky jako realna databaze 


### Struktura testu 
- pro testy si vytvarime virtualni databazy tu muzeme nacitat napr z fictures.json

```python
@skip
```
musim inportovat! a preskakuje def nad kterym je napsany
```python
class ExampleTestCase(TestCase):
    @classmethod
    def setUpTestData(clscls):
    '''spusti se pouze na zacatku a vytvori data pro testy'''

    def setUp(self):
    '''spusti se pred kazdym testem'''

    def test_false(self):
    '''Testovaci metoda '''
    result = False
    self.assertFalse(result)


    def test_add(self):
    result = 1+ 4
    self.assertEqual(result, 5)
```
```python
  @classmethod
    def SetUpTestData
    '''vytvarim data pro jednotlive sloupce tato funkce muze data nacitat jak jenom me napadne'''
```
- vytvarim data pro jednotlive sloupce
- 
## Typy testu 

1. models.py 
    - 

2. forms.py 
   - tyto testy jsou dulezite protoze simuluji inputy od uzivatele
   - pri vazbe many to many myzu v testech vkladat i vice dat najednou 
     - ```python
    'countries': ['1','2'] -> id filmu
    ```


3. testy na gui 
- musime nainstalovat Selenium ( prace s webovou strankou)
```bash
pip install selenium
```
-behem testovani musi byt spusten servet!!

>[!WARNING]
> pracuje s realnou databazi

### Struktura testu
- definuji si prohlizec ktery testuji
  - spustim stranku na serveru
  - otestuji zda je tento text 
```python

```
- test prihlaseni ( tato kontrola je efektivnejsi pomoci test_form.py)
  - vyberu si prohlizec
  - urcim cestu na danou adresu 
  - zadavam ze zdrojoveho kodu stranky presne adresy kam se bude vkladat text
  - 
```python

```
- konec def musi byt assert !


## Selenium 
- da se pouzit k simulaci ze clovek je u pocitace a neco dela. 
- da se nastavit jakakoliv stranka a naprogramovat ukony ktere se maji provadet 