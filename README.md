# Webservers
## zadanie1
### sync test
https://bit.ly/4lyo2PF
### async test
https://bit.ly/3ZZ0eMH

## zadanie2
### sync test
https://bit.ly/44c4QBM
### async test
https://bit.ly/4kkvEVg

## zadanie3
### sync test
https://bit.ly/40zJAU2
### async test
https://bit.ly/3InFckM

# 🧠 Formularze Sync & Async z Celery, Redis, SQLite, Nginx

Ten projekt implementuje system formularzy **synchronicznych i asynchronicznych** z zapisami do bazy danych SQLite oraz obsługą kolejek Celery, z trzema różnymi konfiguracjami:

1. **Flask + uWSGI + Nginx**
2. **Flask + Hypercorn (ASGI) + Nginx**
3. **FastAPI + Uvicorn (ASGI) + Nginx**

---

## ⚙️ Funkcjonalność (wspólna dla wszystkich konfiguracji)

| Endpoint  | Opis                                                                  |
| --------- | --------------------------------------------------------------------- |
| `/sync/`  | Formularz synchroniczny: zapisuje dane bezpośrednio do `sync.db`      |
| `/async/` | Formularz asynchroniczny: dane trafiają do kolejki Celery przez Redis |

**Każda wersja korzysta z tej samej logiki aplikacyjnej** — zmienia się tylko stos serwerowy.

---

## 📦 Technologie

| Komponent                   | Opis                                        |
| --------------------------- | ------------------------------------------- |
| Flask / FastAPI             | Backend aplikacji                           |
| Celery                      | Kolejkowanie zadań                          |
| Redis                       | Broker do Celery                            |
| SQLite                      | Baza danych lokalna (`sync.db`, `async.db`) |
| Nginx                       | Reverse proxy                               |
| uWSGI / Hypercorn / Uvicorn | Serwery aplikacyjne                         |

---

## 🚀 Konfiguracje

### ✅ 1. Flask + **uWSGI** + Nginx

* Wersja klasyczna (WSGI)
* Synchroniczny backend
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

### ✅ 2. Flask + **Hypercorn (ASGI)** + Nginx

* Flask uruchomiony w środowisku ASGI
* Serwer: Hypercorn
* Konfiguracja: `hypercorn.toml`

```toml
bind = ["0.0.0.0:5000"]
workers = 4
timeout = 30
keep_alive_timeout = 5
```

### ✅ 3. FastAPI + **Uvicorn (ASGI)** + Nginx

* W pełni asynchroniczna aplikacja
* Framework FastAPI
* Serwer: Uvicorn (lub Hypercorn)

---

## 📁 Struktura projektu

```
.
├── app/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   └── model.py
├── instance/
│   └── sync.db, async.db
├── main.py
├── celeryWorker.py
├── Dockerfile
├── docker-compose.yml
├── .env
├── uwsgi.ini
└── hypercorn.toml
```

---

## 🔧 Zmienne środowiskowe (`.env`)

```env
FLASK_ENV=development
SECRET_KEY=tajnehaslo

DATABASE_SYNC=sqlite:////instance/sync.db
DATABASE_ASYNC=sqlite+aiosqlite:////instance/async.db

REDIS_URL=redis://redis:6379/0
```

---

## 💪 Uruchomienie (FastAPI domyślnie)

```bash
docker-compose up --build
```

Lub inne konfiguracje:

```bash
docker-compose -f docker-compose-flask-uwsgi.yml up --build
docker-compose -f docker-compose-flask-hypercorn.yml up --build
```

---

## 🔄 Jak działa aplikacja

### `/sync/`

* Użytkownik wypełnia formularz
* Dane zapisywane są bezpośrednio do `sync.db` (SQLite)
* Obsługa synchroniczna

### `/async/`

* Dane trafiają do Celery za pomocą `delay()`
* Celery worker odbiera i zapisuje do `async.db`
* Redis pośredniczy jako broker

---

## 📂 `docker-compose.yml` (fragment)

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./instance:/instance
    env_file:
      - .env
    depends_on:
      - redis

  worker:
    build: .
    command: celery -A celeryWorker.celery_app worker --loglevel=info
    volumes:
      - ./instance:/instance
    env_file:
      - .env
    depends_on:
      - redis

  redis:
    image: redis:7
```

---

## 🌐 Nginx jako reverse proxy

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://web:8000; # lub 5000 dla uWSGI
        include proxy_params;
    }
}
```

---

## ✅ Testowanie

1. Przejdź do `http://localhost/sync/` i `http://localhost/async/`
2. Wypełnij formularz
3. Sprawdź pliki w `instance/` (`sync.db`, `async.db`)
4. Sprawdź logi `celery_worker`, by potwierdzić odbiór

---

## 🧹 Komendy pomocnicze

```bash
docker-compose down -v
docker exec -it fastapi_app sh
sqlite3 /instance/sync.db
```

---

## 📌 Uwagi końcowe

* SQLite nie nadaje się do produkcyjnego zapisu równoległego — używaj PostgreSQL lub MySQL.
* Nie uruchamiaj procesów jako root (Celery ostrzega).
* Nginx pozwala testować różne serwery aplikacji bez zmiany kodu.
