# Contributing to TaskFlow API

## Local setup

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
docker compose up -d db
alembic upgrade head
uvicorn app.main:app --reload
```

## Tests

```bash
pytest -v
```

## Style

- `ruff check app/` must pass
- Pydantic schemas in `app/schemas/`, SQLAlchemy models in `app/models/`
- Database access goes through dependency-injected sessions
- New endpoints must have a corresponding test

## Migrations

```bash
alembic revision -m "describe change" --autogenerate
alembic upgrade head
```
