# Django Python 

dale potrebuji v mem projektu pomoci s vytvorenim uzivatelskych roli mam sice v Django admin 
Authentication and Authorization Groups 
ale moje predstava o pravech je takova ze budu mit role uzivatelu: Admin, Revision Technician, Supervisor for company, 
Company user, a kazde teto skupine budu pridelovat urcite prava co se tyce toho co muzou delat. 
moje predstava je takova ze nekdete view budou vytvoreny primo pro urcite uzivatele aby bylo jednodusi rozdeleni 
context dat atd. jakou formu spravi uzivatelu bych mel pouzit pro efektivni rizeni a mozne rozsireni do budoucna? 


# Postup 
Vytvoření uživatelských rolí v Django může začít tím, že se nadefinují skupiny a určíte jejich oprávnění. 
Jedná se o osvědčený přístup, pokud chcete mít co největší flexibilitu a možnost budoucího rozšíření. 
Django má vestavěný systém autentizace a autorizace, který můžete použít k vytvoření a správě uživatelských rolí a práv.

Zde je, jak můžete pokračovat:

### 1. Definování skupin a oprávnění

Django poskytuje vestavěné modely pro uživatele a skupiny, které můžete použít:

#### Definování práv a skupin

Vytvořte skript, který nastaví vaše skupiny a jejich konkrétní práva. Tímto skriptem můžete například inicializovat databázi po vytvoření.

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Definujte názvy skupin (rolí)
roles = ['Admin', 'Revision Technician', 'Supervisor for Company', 'Company User']

# Vytvořte skupiny, pokud ještě neexistují
for role in roles:
    group, created = Group.objects.get_or_create(name=role)
    
    # Přidejte příslušná oprávnění ke skupinám. Vymyslete vaše vlastní logiku pro udělení oprávnění.
    # Například, můžete vypsat oprávnění, která chcete každé skupině udělit.
    if role == 'Admin':
        # Příklad: udělení všech práv Admin skupině
        permissions = Permission.objects.all()
    elif role == 'Revision Technician':
        # Příklad: seženete oprávnění unikátní pro revizní techniky
        permissions = Permission.objects.filter(codename__in=['view_revisionrecord', 'add_revisionrecord'])
    elif role == 'Supervisor for Company':
        # Specifická oprávnění pro supervizory
        permissions = Permission.objects.filter(codename__in=['view_revisiondata'])
    elif role == 'Company User':
        # Oprávnění pro koncové uživatele společnosti
        permissions = Permission.objects.filter(codename__in=['view_itemgroup'])

    group.permissions.set(permissions)
```

### 2. Asignace uživatelů do skupin

Při vytváření nebo úpravách uživatele v administraci přidáte uživatele do skupiny podle role, kterou by měl mít.

Např.:
```python
from django.contrib.auth.models import User, Group

user = User.objects.get(username='exampleuser')
supervisor_group = Group.objects.get(name='Supervisor for Company')
user.groups.add(supervisor_group)
```

### 3. Použití skupin a oprávnění ve view

Přidejte kontrolu oprávnění do vašich pohledů pomocí dekorátoru `user_passes_test`, mixinů jako `PermissionRequiredMixin`, nebo si vytvořte vlastní logiku na zpracování uživatelských rolí.

#### Použití `PermissionRequiredMixin`

```python
from django.contrib.auth.mixins import PermissionRequiredMixin

class SomeProtectedView(PermissionRequiredMixin, View):
    permission_required = 'app_name.permission_codename'
    
    def get(self, request, *args, **kwargs):
        # zde bude váš kód pro GET…
```

#### Použití dekorátoru `user_passes_test`

```python
from django.contrib.auth.decorators import user_passes_test

def check_supervisor(user):
    return user.groups.filter(name='Supervisor for Company').exists()

@user_passes_test(check_supervisor)
def supervisor_view(request):
    # váš kód pro view
```

### 4. Budoucí rozšíření

Plánujete-li rozšíření, ujistěte se, že vaše oprávnění nejsou příliš těsně svázána s aktuálními funkcionalitami. 
Mohou se například změnit právní požadavky nebo architektonické změny, které ovlivní vaši aplikační logiku. 
Buďte připraveni na refaktoring podle změn v potřebách vašich uživatelů.

Tento přístup vám umožňuje flexibilně řídit uživatelská oprávnění a s růstem projektu můžete přidávat nové role 
nebo měnit jejich oprávnění, aniž byste zasahovaly do implementace samotných pohledů.


# HTML

a jak osetrim tyto role v templates aby se urcitym uzivatelum zobrazovali pouze urcite tlacitka atd. 


## Posup
Pro zajištění, že se určitá tlačítka nebo části obsahu zobrazují pouze uživatelům s konkrétními rolemi, můžete v 
Django šablonách používat rozhodovací logiku a vestavěné filtry a tagy. Zde je několik způsobů, jak toho dosáhnout:

### 1. Použití šablonových tagů a filtrů

Django poskytuje tagy, jako například `{% if %}` a `{% ifequal %}`, které vám umožňují kontrolovat podmínky přímo v šablonách:

#### Příklad: Kontrola příslušnosti ke skupině

```html
{% if user.is_authenticated %}
    {% if 'Admin' in user.groups.all|pluck:'name' %}
        <!-- Tlačítka viditelná pouze pro Admina -->
        <a href="{% url 'admin_dashboard' %}" class="btn btn-primary">Admin Dashboard</a>
    {% endif %}

    {% if 'Supervisor for Company' in user.groups.all|pluck:'name' %}
        <!-- Tlačítka viditelná pouze pro Supervisor for Company -->
        <a href="{% url 'supervisor_dashboard' %}" class="btn btn-warning">Supervisor Dashboard</a>
    {% endif %}
    
    <!-- Všichni přihlášení uživatelé uvidí následující tlačítko -->
    <a href="{% url 'user_profile' %}" class="btn btn-info">Profile</a>
{% endif %}
```

### 2. Vytvoření vlastního šablonového filtru

Pokud plánujete kontrolovat role často, můžete si vytvořit vlastní šablonový filtr, který kontroluje, zda uživatel patří do určité skupiny:

#### Definujte vlastní filtr

Vytvořte soubor `templatetags/user_extras.py` ve vaší aplikaci:

```python
from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
```

Ve vaší šabloně nezapomeňte tento filtr zavést a používat:

```html
{% load user_extras %}

{% if user|has_group:"Admin" %}
    <!-- Obsah viditelný pouze pro adminy -->
    <a href="{% url 'admin_dashboard' %}" class="btn btn-primary">Admin Dashboard</a>
{% endif %}

{% if user|has_group:"Supervisor for Company" %}
    <!-- Obsah viditelný pouze pro supervizory -->
    <a href="{% url 'supervisor_dashboard' %}" class="btn btn-warning">Supervisor Dashboard</a>
{% endif %}
```

### 3. Použití stavů ve view a kontextu

Můžete také přidat logiku na úrovni view a poskytovat specifické proměnné do kontextu šablony. Na základě těchto proměnných pak řídit, co se uživatelům zobrazí:

#### Logika ve view

```python
def some_view(request):
    context = {}
    if request.user.groups.filter(name='Admin').exists():
        context['is_admin'] = True
    
    if request.user.groups.filter(name='Supervisor for Company').exists():
        context['is_supervisor'] = True
    
    return render(request, 'template.html', context)
```

#### Podmíněný obsah v šabloně

```html
{% if is_admin %}
    <!-- Tlačítka pro Adminy -->
    <a href="{% url 'admin_dashboard' %}" class="btn btn-primary">Admin Dashboard</a>
{% endif %}

{% if is_supervisor %}
    <!-- Tlačítka pro Supervisor for Company -->
    <a href="{% url 'supervisor_dashboard' %}" class="btn btn-warning">Supervisor Dashboard</a>
{% endif %}
```

Tímto způsobem můžete zajistit, že se specifické části UI zobrazí pouze uživatelům s danými oprávněními, čímž se zlepší uživatelská zkušenost a zjednoduší údržba kódu.
