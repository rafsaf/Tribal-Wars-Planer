## Link do strony

- [www.plemiona-planer.pl](https://www.plemiona-planer.pl/pl/)

## Link do discorda

- [discord.gg/g5pcsCteCT](https://discord.gg/g5pcsCteCT)

Opis instalacji

Najlepiej korzystać z dockera, w razie gdyby go nie było, wystarczy w settings.py zmienić host, nazwę czy cokolwiek postgresa na wybrane - lokalne.

1. Używać python 3.6.8 lub 3.6.9, tutaj instalacja https://www.python.org/downloads/release/python-368/
2. Pobrać repozytorium, najlepiej na wybranym branchu, np. dla v1.05

```bash
git clone https://github.com/rafsaf/Plemiona_Planer.git -b v1.05
```

2. Utworzyć plik `settings.py` pod ścieżką `django_plemiona/settings.py` i skopiować tam wzór z `django_plemiona/settings.txt` a następnie ewentualnie pozmieniać SECRET_KEY (i jak na początku wspomniane, ewentualnie ustawienia bazy danych - domyślnie pointują one w host który zrobi docker, poniżej zamieszczam obecne ustawienia pod lokalną instalację z racji że od dziś w settings.txt są ustawienia pod dockera).

```python
# Stare ustawienia domyślne
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "django_plemionav05",
        "USER": "rafsaf",
        "PASSWORD": "123",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
```

3. Wybranym sposobem utworzyć virtualenv w głównym folderze projektu, koniecznie dla 3.6, dla konwencji najlepiej korzystać z czegoś takiego i nazywać to jak poniżej

```bash
py -3.6 -m venv venv
python -3.6 -m venv venv
```

4. Uruchomić virtualenv, VS Code robi to autmatycznie więc najlepiej w ten sposób ale można też

```
# windows
.\venv\Scripts\activate


# linux
source venv/bin/activate


# nastepnie zainstalować cały syf

pip install -r requirements.txt

```

5. następnie ożywić postgresa z dockera (chodzi na nieużywanym często porcie 5000 więc nie powinno być problemów z czymś innym, w szczególności z zwykłą instlacją postgresa zwyczajowo na porcie 5432)

```
docker-compose up
```

6. Baza już działa, wystarczyć powinno uruchomienie projektu na localhost:8000 po wcześniejszym utworzeniu superusera admin-admin i migracjach

```bash
python manage.py test
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# potem admin / admin itd.
python manage.py runserver

```

Raczej działa :)

7. Test coverage

```bash
pip install coverage

coverage run --source='.' --omit 'venv/*,*tests*' manage.py test

coverage report
```

8. .env for production
```
DEBUG="false"
ALLOWED_HOSTS="plemiona-planer.pl,www.plemiona-planer.pl"
SECRET_KEY="secret_key_here"
POSTGRES_NAME="postgres"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
EMAIL_BACKEND="django_ses.SESBackend"
AWS_ACCESS_KEY_ID="AKIAU5MB5PQDND3JDQMH"
AWS_SECRET_ACCESS_KEY="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"
AWS_SES_REGION_NAME="eu-central-1"
AWS_SES_REGION_ENDPOINT="email.eu-central-1.amazonaws.com"
DEFAULT_FROM_EMAIL="plemionaplaner.pl@gmail.com"
RECAPTCHA_PUBLIC_KEY="6LfTofUZAAAAAIFiXfroDC4NtxnHlXqMMHx4jiQJ"
RECAPTCHA_PRIVATE_KEY="6LfTofUZAAAAAOPybWlY4WLU4G0v2YwcLvwLRfIH"
```
