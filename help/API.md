# Api čerpání z jiných stránek
- mohu omezit pocet dotazu na Api 
- vysledek dotazu API uložím do databáze 
  - podle potřeby přímo k uživateli do tabulkz Profil
  - pro celou stranku s podmínkami jak často se mají aktualiyovat data


# Api poskytování dat jiným stránkám 
- Instalace nové aplikace 
```bash
python manage.py startapp api
```
instalace nove knihovny 
```bash
pip install djangorestframework
```
# serializers.py
- nahrazuje forms.py 

```python
from rest_framework import serializers

from viewer.models import Movie, Creator


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        #fields = ['title_orig', 'title_cz', 'year']
        fields = '__all__'


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'
```
  - obdoba forms.py
  - čerpá data z models.py

# views.py
  - **mixins** 
    - Poskytují předpřipravenou logiku pro konkrétní operace
      - **RetrieveModelMixin**: Přidává podporu pro získání jednoho objektu (HTTP metoda GET).
      - **UpdateModelMixin**: Přidává podporu pro aktualizaci objektu (HTTP metoda PUT nebo PATCH).
      - **DestroyModelMixin**: Přidává podporu pro mazání objektu (HTTP metoda DELETE).
      - **mixins.ListModelMixin**: 
        - Tento mixin poskytuje metodu pro zobrazení seznamu objektů (obvykle odpovídá HTTP metodě GET na kolekci objektů, např. /api/movies/).
        - Používá se, když chcete vytvořit endpoint, který vrací všechny položky z databáze, často ve spojení s paginací, filtrováním nebo řazením.
        - Když potřebujete pouze číst (zobrazovat seznam) dat a nechcete implementovat celou logiku sami.
        - Vhodné pro seznamy dat v aplikaci, například seznam článků, filmů nebo uživatelů.
      - **mixins.CreateModelMixin**:
        - Tento mixin poskytuje metodu pro vytvoření nového objektu (odpovídá HTTP metodě POST).
        - Používá se, když chcete vytvořit endpoint, který umožňuje přidání nové položky do databáze.
        - Když chcete vytvořit jednoduchý endpoint pro přidávání nových dat.
        - Vhodné pro API umožňující uživatelům vytvářet nové záznamy, jako je registrace, přidání komentáře, atd.

  - **generic** 
    - (obecné třídy) v DRF jsou předpřipravené základní pohledy (views), které kombinují mixins a poskytují 
    nejčastěji používané funkce. Umožňují rychlé vytvoření API bez nutnosti psát opakující se kód.
    - **GenericAPIView**: Základní generická třída pro přizpůsobení mixinů.
    - **RetrieveAPIView**: Automaticky poskytuje metodu GET pro získání jednoho objektu.
    - **UpdateAPIView**: Automaticky poskytuje metodu PUT nebo PATCH pro aktualizaci objektu.
    - **DestroyAPIView**: Automaticky poskytuje metodu DELETE pro mazání objektu.
      
- urls.py -> definuji cestu k filmům 


# Mobilni aplikace pomocí API
- když chci ke stránce přidat aplikaci používám API 


## API permisions

# settings.py  
  - INSTALED_APPS 
```python
'rest_framework',
'api',
```
  - REST_FRAMEWORK 
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ]
}
```
- recikluji permisions z Django accounts 


# urls.py
- import z api.views
```python
from api.views import Movies, MovieDetail, Creators, CreatorDetail
# cesty pro API
    path('api/movies/', Movies.as_view(), name='api_movies'),
    path('api/movie/<pk>/', MovieDetail.as_view(), name='api_movie'),
    path('api/creators/', Creators.as_view(), name='api_creators'),
    path('api/creator/<pk>/', CreatorDetail.as_view(), name='api_creator'),
```