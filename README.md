# TaskFlow

Учебный трекер задач на FastAPI + Vue.

## GitHub Actions (ЛР №3)

В проекте настроен pipeline GitHub Actions в `.github/workflows/ci-cd.yml`.

Что делает pipeline:

- запускает функциональный backend-тест CRUD;
- собирает frontend;
- проверяет `docker-compose.yml` с переменными окружения;
- собирает Docker-образы;
- при push в `main` публикует Docker-образы в GHCR.

### Variables и Secrets для GitHub

В репозитории GitHub откройте `Settings -> Secrets and variables -> Actions` и создайте:

Variables:

- `APP_NAME`
- `API_PREFIX`
- `CORS_ORIGINS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `BACKEND_PORT`
- `FRONTEND_PORT`

Secret:

- `POSTGRES_PASSWORD`

Рекомендуемые значения:

- `APP_NAME` = `TaskFlow API`
- `API_PREFIX` = `/api/v1`
- `CORS_ORIGINS` = `["http://localhost:8080","http://127.0.0.1:8080","http://localhost:5173","http://127.0.0.1:5173"]`
- `POSTGRES_DB` = `taskflow`
- `POSTGRES_USER` = `taskflow_user`
- `BACKEND_PORT` = `8000`
- `FRONTEND_PORT` = `8080`
- `POSTGRES_PASSWORD` = `taskflow_password` (Secret)

## Docker

Frontend теперь работает без Nginx:

- `backend/` — FastAPI API;
- `frontend/` — Vue, собирается через Vite и отдается Node-сервером `serve`;
- `db/` как отдельного каталога нет, БД запускается сервисом PostgreSQL из `docker-compose.yml`.

### Запуск

```bash
cp .env.example .env
docker compose up --build
```

После запуска:

- frontend: `http://localhost:8080`
- backend: `http://localhost:8000`
- health: `http://localhost:8000/health`

### Важно

Если вы меняли пароль PostgreSQL в `.env`, а volume уже был создан, старая БД останется со старым паролем.
Для полной переинициализации:

```bash
docker compose down -v
docker compose up --build
```
