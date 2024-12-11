from django.forms.models import ModelForm
#Vkladani souboru
- pokud chci vlozit neco jineho nez image muzu pouzit FileField
  - musime ale myslet na to jak se tento soubor bude zobrazovat
- image muze byt v jakemkoli modelu v models.py
# Přidání obrázků do databaze 
- Django umi pracovat s obrazky naprimo
- Nainstalovat Pillow knihovnu
- slozka Images se vytvori sama
```bash
pip install Pillow 
```
- v models.py vytvorime 'ImageField'
    - obrazek samotny musime samy nekam vlozit 
    - settings.py nastavim MEDIA_ROOT
```Python
MEDIA_ROOT = BASE_DIR
MEDIA_URL = 'images/'
```
do urls.py 
```python
urlpatterns = [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
- na konec seznamu urlpatterns = [
- admin.py admin.site.register(Image)


## Funkce obrazku 
- muzu si udelat klikaci obrazek pomoci odkazu <a href=
  - models.py pridame class Image(Model): 
  - image.html -> vytvorim template kde se bude obrazek zobrazovat 
  - musime v urls.py definovat url cestu k obrazku 


## Vkladani obrazku
- template -> form.html
  - musime jeste pridat enctype kvuli funkci odesilani
```python

```
- forms.py 
```python
class ImageModelForm(ModelForm):
    class Meta:
```
- views.py
  - Create, Update, Delete
- url.py

