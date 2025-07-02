# Formularze Sync & Async z Celery, Redis, SQLite, Nginx

Implementacja systemu formularzy **synchronicznych i asynchronicznych** z zapisami do bazy danych SQLite oraz obsługą kolejek Celery (asyc), z trzema różnymi konfiguracjami:

1. **Flask + uWSGI + Nginx**
2. **Flask + Hypercorn (ASGI) + Nginx**
3. **FastAPI + Uvicorn (ASGI) + Nginx**

---

## Funkcjonalność (wspólna dla wszystkich konfiguracji)

| Endpoint  | Opis                                                                  |
| --------- | --------------------------------------------------------------------- |
| `/sync/`  | Formularz synchroniczny: zapisuje dane bezpośrednio do `sync.db`      |
| `/async/` | Formularz asynchroniczny: dane trafiają do kolejki Celery przez Redis |

**Każda wersja korzysta z tej samej logiki aplikacyjnej** — zmienia się tylko stos serwerowy.

---

## Technologie

| Komponent                   | Opis                                        |
| --------------------------- | ------------------------------------------- |
| Flask / FastAPI             | Backend aplikacji                           |
| Celery                      | Kolejkowanie zadań                          |
| Redis                       | Broker do Celery                            |
| SQLite                      | Baza danych lokalna (`sync.db`, `async.db`) |
| Nginx                       | Reverse proxy                               |
| uWSGI / Hypercorn / Uvicorn | Serwery aplikacyjne                         |

---

## Struktura projektu

Występowanie niektórych plików jest zależne od konfiguracji 

```
.
├── app/
│   ├── forms/ # pliki konfiguracji formularza
│   ├── routes/ # pliki odpowiedzialne za zachowanie endpointów
│   ├── templates/ # pliki html
│   ├── static/ # plik loader oraz css
│   ├── model.py # pliki konfiguracji modelów baz danych
│   └── __init__.py # dla konfiguracji Flask
├── instance/
│   └── sync.db, async.db
├── main.py # główny plik
├── celeryWorker.py  # obsługa celery
├── Dockerfile # konfiguracja obrazu flask_app lub fastapi_app
├── docker-compose.yml # plik konfiguracji środowiska 
├── .env 

```

---
## Zmienne środowiskowe (przykład)

```env
FLASK_ENV=development
SECRET_KEY=supertajnehaslo # można zaimpelentować przechowywanie i odczyt hashu np.: sha256

DATABASE_SYNC=sqlite:////instance/sync.db
DATABASE_ASYNC=sqlite:////instance/async.db # (dla FASTAPI DATABASE_ASYNC=sqlite+aiosqlite:////instance/async.db)
REDIS_URL=redis://redis:6379/0
```
---
## Testowanie
### Użyto narzędzia ze strony loader.io [LINK]((https://loader.io/)), testy wykonywano na 100 wejścia w ciągu 1 minuty.

---

## Konfiguracje

### 1. Flask + **uWSGI** + Nginx

* Wersja klasyczna (WSGI)
* Konfiguracja serwera: `uwsgi.ini`

```ini
[uwsgi]
module = main:app
callable = app
master = true
processes = 4
http = 0.0.0.0:5000
vacuum = true
die-on-term = true
```

### Wyniki testów
[SYNC](https://bit.ly/44c4QBM)
[ASYNC](https://bit.ly/3ZZ0eMH)

### 2. Flask + **Hypercorn (ASGI)** + Nginx

* Flask uruchomiony w środowisku ASGI
* Serwer: Hypercorn
* Konfiguracja: `hypercorn.toml`

```toml
bind = ["0.0.0.0:5000"]
workers = 4
timeout = 30
keep_alive_timeout = 5
```

### Wyniki testów
[SYNC](https://bit.ly/40zJAU2)
[ASYNC](https://bit.ly/4kkvEVg)

### 3. FastAPI + **Uvicorn (ASGI)** + Nginx

* Framework FastAPI
* Serwer: Uvicorn

### Wyniki testów
[SYNC](https://bit.ly/4lyo2PF)
[ASYNC](https://bit.ly/3InFckM)

---

## Uruchomienie 

Każdą konfiguracje można uruchomić za pomocą pliku `docker-compose.yml`, powstają następujące kontenery:
1. Flask_app lub FastAPI_app
2. Nginx
3. Redis
4. Celery

```bash
docker compose up --build # docker-compose up --build -> w zależności od wersji - Dockerem (>= 20.10) domyślnie działa docker compose
```

---

## Jak działają endpointy

### `/sync/`

* Użytkownik wypełnia formularz
* Dane zapisywane są bezpośrednio do `sync.db` (SQLite)
* Obsługa synchroniczna

### `/async/`

* Dane trafiają do Celery za pomocą `delay()`
* Celery worker odbiera i zapisuje do `async.db`
* Redis pośredniczy jako broker

---


## Nginx jako reverse proxy
##### Plik konfiguracyjny `nginx.conf` definiuje serwer HTTP, który działa jako **reverse proxy** dla aplikacji backendowej (Flask lub FastAPI). Przekazuje żądania HTTP z portu 80 do aplikacji uruchomionej na porcie 5000 lub 8000 w kontenerze `flask_app` lub `fastapi_app`. Konfiguracja posiada kilka parametrów, które mają zapewnić podstawową ochronę danych, posiada także konfiguracje logów oraz bezpieczeństwo nagłówków.
---

## Komendy dodatkowe

```bash
docker exec -it fastapi_app sh # uruchomienie powłoki bash kontenera
sqlite3 /instance/sync.db # operacje na bazie
docker-compose down -v # zatrzymanie i usunięcie kontenerów + wolumenów 
docker-compose down --remove-orphans # zatrzymania i usunięcia kontenerów wraz z pozostałoścami po poprzednim uruchomieniu docker-compose.yml
docker-compose rm -f  # usuwanie kontenerów (force)
docker system prune -af  # usuwanie wszystkiech kontenery, sieci, cache
docker-compose logs -f  # logi ze wszystkich usług
docker-compose logs -f web # logi z aplikacji webowej
docker ps -a  # pokazanie wszystkich kontenerów
docker volume ls # lista wolumenów
docker network ls # lista sieci
```

---

## Uwagi końcowe i rzeczy do poprawy/dodania

* SQLite nie nadaje się zbyt do tego. Lepiej już PostgreSQL
* Celey powinno się używać nie jako root.
* Należy zadbać o optymalizacje pod konkretny serwer aplikacyjny dodająć odpowienie parametry do Nginxa.
* Dodanie certyfikacji HTTPS aby zapewnić szyfrowane połączenie.
* Poprawa walidacji formularzy, np.: użycie pydatic
* Dokładniejsze zbieranie logów: Grafana, Flower
