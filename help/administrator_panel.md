# Upravy ve zobrazeni administracniho panelu 
- v aplikaci
  - u nas viewer/admin.py 
  ## ListViewes
    - muzu definovat jak se budou zobrazovat data 
    - cerpam data z viewer/models.py 
    - muzu take nastavit ktere polozky jsou klikatelne a odkazuji 
    - kolik veci se mi zobrazi na jedne strance 
    - filtrovani podle jednotlivych parametru
    - pridat vyhledavaci okno 
    - actions 
        - pridam akce ktere muzu provadet 
        - muzu vybirat klidne vice polozek a provadet u nich mnou definovane funkce
  ## Formview
    - nastavujeme format jak se zobrazuje formular pro vkladani a upravu dat
      - muzeme rozdelit kolonky pro vkladani dat do skupin ktere budou jeste podrobneji specifikovane 
    - muzu zde napriklad omezit co muze administrator upravovat -> readonly
      - napriklad datum zapisu a upravy nemuze menit ani admin. 