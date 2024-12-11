nepouzivat nazev user!!
vazba one to one

v account/models.py

vytvorim class

account/forms.py

zaregistruji v accounts/admin

musim provest migrace protoze jsem upravoval databaze


pro migrace je dobre mit vlastni branche

nebo mit migrace v git ignor a delat migrace v kazde branche znovu. a v dalsi branche musim zase udelat migrace

rozsirime si form.registration o tyto dalsi data ktere jsme definoval v profile

pozor odkud importuji

accounts/forms.py pridam data ktera z account/models.py

    def save(self): ulozi noveho uzivatele jak do profile tak do users. v admin sekci stranky
        tato metoda musim byt @atomick aby se nestalo ze se potkaji dva uzivatele ve stejny cas


user = uzivatelska data heslo a prava

Profile = informace o uzivateli