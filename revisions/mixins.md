Dekorátory jsou v Pythonu funkce, které umožňují změnit chování jiné funkce nebo metody. Jsou velmi užitečné pro opakované vzory nebo pro přidání další funkcionality bez nutnosti upravovat původní kód.

#### Příklad použití dekorátoru pro `form_valid` a `form_invalid`

Řekněme, že chceme logovat každé úspěšné nebo neúspěšné uložení formuláře. Můžeme vytvořit dekorátor, který to zajistí:

```python
import logging

# Nastavíme logger
logger = logging.getLogger(__name__)

def log_form_activity(log_message):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            
            # Logovat zprávu
            logger.info(log_message.format(self.__class__.__name__))
            
            return response
        return wrapper
    return decorator

class CreateMixin(CreateView):
    success_message = 'The item was successfully saved from CreateMixin'
    error_message = 'error message from CreateMixin'
    warning_message = 'warning message from CreateMixin'

    @log_form_activity('Form valid in {}')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, self.success_message)
        return redirect(self.request.path)

    @log_form_activity('Form invalid in {}')
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.error_message:
            messages.error(self.request, self.error_message)
        return response
```

#### Výhody použití dekorátorů:

1. **Znovupoužitelnost kódu:** Dekorátory mohou být znovu použity různými třídami nebo metodami, což zlepšuje čitelnost a údržbu kódu.
  
2. **Oddělení funkcionality:** Dekorátory umožňují oddělit kód, který vykonává specifické funkce, od hlavní logiky, což usnadňuje ladění a rozšíření.

3. **Konzistence:** Pokud provádíte stejné činnosti na více místech (například validace, logování), dekorátory mohou pomoci zajistit, že se tyto činnosti provádějí stejným způsobem.

Pokud se dekorátor použije na více místech, můžete jeho logiku centralizovat a snadno upravit podle potřeby, aniž byste měnili kód všude tam, kde je použit.

