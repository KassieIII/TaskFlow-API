# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed
- CI simplified: dropped the PostgreSQL service and Alembic step — current
  health/OpenAPI tests are stateless and don't need a live database.

### Added
- `pyproject.toml` with `pytest` configuration (`pythonpath`, `testpaths`).

### Fixed
- Ruff F401/F821/E712 across `app/models/*` and `app/routers/*`.

## [0.1.0] - 2026-04-20

### Added
- FastAPI scaffolding with health-check and OpenAPI schema endpoints.
- SQLAlchemy 2.0 async models for users, projects and tasks.
- Alembic migrations with initial schema.
- JWT auth scaffolding (`python-jose`, `passlib[bcrypt]`).
- Dockerfile and `docker-compose.yml` for local development.
