# tabulka pro ukladani dat 




# definice modelu 
- viewer/model.py 
- viewer/views.py
  - class MovieTemplateView
  - def get_context_data zde resim odesilani formulare s hodnocenim
    - zpracovava data formulare a vraci rating 
  - def post zde spracovavam data vlozena uzivatelem
    - movie ->zde si vytahnu informace o movie z contextu
    - reviewer -> musim vytahnout s Profile z accounts
    - rating_avg -> odkazuji z models.py/class Rewiew na tabulku s hodnocenim a spocitam prumer hodnoceni
    - kontroluji zde aby nemohl uzivatel hodnotit vicekrat movie_ = Review.objects.filter
      - pokud uz ma komentar prepise -> edit
- uprava movie.html 
  - pridam sekci kde se zobrazi formular pro hodnoceni 
  - vytvorim pole ve kterem se budou zobrazovat hodnoceni 
    - zde budu zobrazovau uzivatele, datum vlozeni (upravim format), 
