# Identifikační údaje:

- username (CharField): Uživatelské jméno.
- first_name (CharField): Křestní jméno uživatele (nepovinné).
- last_name (CharField): Příjmení uživatele (nepovinné).
- email (EmailField): E-mailová adresa (nepovinné).
# Autentizační údaje:

- password (CharField): Hash hesla uživatele.
- is_staff (BooleanField): Určuje, zda má uživatel přístup do Django admin rozhraní.
- is_superuser (BooleanField): Určuje, zda má uživatel všechna oprávnění.
- is_active (BooleanField): Určuje, zda je účet aktivní (např. deaktivovaný uživatel nebude mít přístup).
- last_login (DateTimeField): Datum a čas posledního přihlášení uživatele.
- date_joined (DateTimeField): Datum a čas vytvoření uživatelského účtu.

# Skupiny a oprávnění:

- groups (ManyToManyField): Skupiny, do kterých uživatel patří (např. pro role nebo oprávnění).
- user_permissions (ManyToManyField): Individuální oprávnění přiřazená uživateli.


# Další metody modelu User:
- set_password(raw_password): Nastaví hash hesla.
- check_password(raw_password): Ověří, zda dané heslo odpovídá hashovanému heslu.
- get_full_name(): Vrátí celé jméno (křestní + příjmení).
- get_short_name(): Vrátí křestní jméno.