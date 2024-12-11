

# forms.py

- omezime vkladanou hodnotu
```python
from django.db.models import IntegerField

class ReviewModelForm():
    rating = IntegerField(min_value=1, max_value=10)
```
musím správně odsadit pod class 1 Tab!!!!
