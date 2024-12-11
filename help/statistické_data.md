# Počítání návštěvnosti

## zobrazení
- pro každou položky u které chci znát počet zobrazení 
  - **models.py**
    - přidám položku do tabulky u modelu a tím si každá položka bude ukladat počet zobrazení 
    - přidám kolonku (page_views)
```python
page_views = IntegerField(default=0)
```
 - **movie.html**
   - pokud chci na stránce uživately ukázat počet zobrazení pridám tuto položku na template
    ```html
    Počet zobrazení filmu: {{ movie.page_views }}.
    ```
 - **views.html**
    - **def get** (zobrazovací funkce)
    - přidám funkci pro ukládání počtu zobrazení ( při každém zavolání určité views)
    ```python
     movie_ = Movie.objects.get(id=pk)
     movie_.page_views = movie_.page_views + 1
     movie_.save()
    ``` 