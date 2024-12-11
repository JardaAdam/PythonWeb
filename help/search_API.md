# urls.py
```python
from viewer.views import search
  path('search/', search, name='search'),
```
# pro spojeni s Googlem 
- potřebuji zažádat o klíč pro API 
- https://developers.google.com/custom-search/v1/introduction

## Google API 
- views.py -> definuji funkci pro vyhledávání 
```python
from dotenv import load_dotenv
import requests
load_dotenv()
def search(request):
    if request.method == 'POST':  # pokud jsme poslali dotaz z formuláře
        search_string = request.POST.get('search').strip()
        if len(search_string) > 0:
            movies_title_orig = Movie.objects.filter(title_orig__contains=search_string)
            movies_title_cz = Movie.objects.filter(title_cz__contains=search_string)
            # TODO Vyhledávat filmy podle description
            # TODO Vyhledávat tvůrce podle jména
            # TODO Vyhledávat tvůrce podle příjmení
            # Google API
            url = f"https://www.googleapis.com/customsearch/v1?key={os.getenv('GOOGLE_API_KEY')}&cx={os.getenv('GOOGLE_CX')}&q={search_string}"
            g_request = requests.get(url)
            g_json = g_request.json()
            """print(g_json)
            for g_result in g_json["items"]:
                print(g_result['title'])
                print(f"\t{g_result['link']}")
                print(f"\t{g_result['displayLink']}")
                print(f"\t{g_result['snippet']}")"""
            context = {'search': search_string,
                       'movies_title_orig': movies_title_orig,
                       'movies_title_cz': movies_title_cz,
                       'g_json': g_json}
            return render(request, 'search.html', context)
    return render(request, 'home.html')
```
  - do .env uložím přístupové údaje a v programu ve views.py již volám pouze nazev pod 
 kterým jsem reálné údaje uložil v .env
  - data z googlu chodí jako .json soubory
  - import requests a nainstaluji request

- search.html -> přidám pole pro zobrazování výsledků z google
```html
{% extends "base.html" %}
{% block content %}
<h1>Výsledky vyhledávání výrazu: '{{ search }}'</h1>
    <h2>Výsledky pro originální název</h2>
    <ul>
        {% for movie in movies_title_orig %}
            <li><a href="{% url 'movie' movie.id %}">{{ movie.title_orig }}</a></li>
        {% endfor %}
    </ul>
    <h2>Výsledky pro český název</h2>
    <ul>
        {% for movie in movies_title_cz %}
            <li><a href="{% url 'movie' movie.id %}">{{ movie.title_cz }}</a></li>
        {% endfor %}
    </ul>
    {% if g_json %}
        <h2>Výsledky vyhledávání na ČSFD.cz</h2>
        <ul>
            {% for g_result in g_json.items %}
                <li><a href="{{ g_result.link }}">{{ g_result.title }}</a><br>
                    {{ g_result.snippet }}
                </li>
            {% endfor %}
        </ul>
    {% endif %}
{% endblock %}
```
  - 

# Navbar.html
- vložím nový <div> pro vzhledávání na stránce 
```html
            <div class="navbar-nav ml-auto">
                <div id="search-div">
                    <form method="post" action="/search/">
                        {% csrf_token %}
                        <input type="text" id="search" name="search" placeholder="🔎 Hledej...">
                    </form>
                </div>
            </div>
```

