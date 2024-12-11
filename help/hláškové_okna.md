- abych zamezil přesměrovánímu uživateli bez určitých práv na error stranku 
- vytvořím template 403.html 
# HTML errors
- ošetření těchto hlášek (400, 403, 404, 5**)
- vztvořím templates s nazvem chybové hlášky 
  - díky tomu zůstane Navbar a základní design stránky pouze se zobrazí námi definovaná hláška 

- musím v settings.pz přepnout DEBUG -> False
```python
ALLOWED_HOSTS = ['127.0.0.1']
```

# příklady zobrazení hlášky 
- 400 -> Chybné parametry v URL
```bash
http://127.0.0.1:8000/api/user?id=123
```

- 403 -> uživatel nemá oprávnění pro vztváření 
```bash
http://127.0.0.1:8000/movie/create/
```
- 404 -> špatný formát URL adresy 
```bash
http://127.0.0.1:8000/movi
```
