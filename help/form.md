forms.py

zde se vytvari formulare pro manipulaci dat uzivatelem -> vkladani, mazani, uprava

je potreba udelat .html soubor pro formular!!

v tomto souboru se daji osetrit zadavana data - umrti pred narozenim, narozeni v budoucnu atd.

urls.py
je potreba zadat cestu k formulari do souboru !! cesta neni primo do form.py ale do views.py a tam se
class CreatorFormView(FormView): odkazuje do forms.py na class CreatorForm(ModelForm):


Cleanup a validation!!!
muzeme zadavat ruzne funkce pro kontrolu a upravu textu ktery uzivatel zadal


da se pracovat se strukturou formulare a rozlozenim chybovich hlasek atd.

Forms own design

Tags {%   %}

Variables {{  }}


Filters

umornuji v html souboru upravovat zobrazovani dat


i18n vicejazycne preklady



