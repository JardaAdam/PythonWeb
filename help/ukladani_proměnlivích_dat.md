Aby se při kažném otevření stránky nespouštěli funkce které počítají 
- průměrné hodnocení filmu přidám
  - models.py do Movies kolonka **rating** která ukládá a přepisuje tuto hodnotu
  ```python
  from django.db.models import FloatField
  rating = FloatField(null=True, blank=True)
  ```
  - views.py do metody 
    - def post přidám ukládání této hodnoty do databáze
    ```python
    movie_.rating = rating_avg
    movie_.save()
    ```
    - get_context_data upravim cestu pro ulozeni vysledku prumerneho hodnoceni
    ```python
    context['rating_avg'] = movie_[0].rating
    ```

# zaokrouhlování výstupu 
1. zadám do výpočtu na kolik desetiných míst má počítat
2. v templates omezím zobrazení dat. (movie.html)
```python
 {{ rating_avg|floatformat:1 }}
```