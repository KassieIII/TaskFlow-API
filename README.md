# ✅ TaskFlow API

![CI](https://github.com/KassieIII/taskflow-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)
![License](https://img.shields.io/badge/license-MIT-green)

A clean REST API for task and project management built with FastAPI. Features JWT authentication, role-based access, and real-time status tracking.

## Features

- **JWT Authentication** — Secure login/register with token refresh
- **Projects** — Create, update, archive projects
- **Tasks** — Full CRUD with status workflow (todo → in_progress → review → done)
- **Assignments** — Assign tasks to team members
- **Filtering & Pagination** — Search, sort, filter by status/assignee/priority
- **Role-Based Access** — Admin, manager, member roles

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Alembic (migrations)
- Pydantic v2 (validation)
- JWT (python-jose)

## Quick Start

### With Docker (recommended)

```bash
docker-compose up --build
```

API runs at `http://localhost:8000`. Migrations run automatically.

### Local development

```bash
# Clone
git clone https://github.com/KassieIII/taskflow-api.git
cd taskflow-api

# Install
pip install -r requirements.txt

# Set env
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

Health checks:

- `GET /health` — application liveness for humans and dashboards
- `GET /healthz` — lightweight liveness alias for containers and probes

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token TTL (default: 30) |

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login, get JWT token |
| GET | `/api/v1/auth/me` | Get current user |

### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/projects` | List user's projects |
| POST | `/api/v1/projects` | Create project |
| GET | `/api/v1/projects/{id}` | Get project details |
| PATCH | `/api/v1/projects/{id}` | Update project |
| DELETE | `/api/v1/projects/{id}` | Archive project |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/projects/{id}/tasks` | List tasks (filter, sort, paginate) |
| POST | `/api/v1/projects/{id}/tasks` | Create task |
| GET | `/api/v1/tasks/{id}` | Get task |
| PATCH | `/api/v1/tasks/{id}` | Update task |
| DELETE | `/api/v1/tasks/{id}` | Delete task |
| PATCH | `/api/v1/tasks/{id}/status` | Change status |
| PATCH | `/api/v1/tasks/{id}/assign` | Assign to user |

## Project Structure

```
taskflow-api/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app setup
│   ├── config.py          # Settings from env
│   ├── database.py        # SQLAlchemy engine & session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── projects.py
│   │   └── tasks.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   └── dependencies.py    # Auth dependency injection
├── alembic/
│   └── ...
├── tests/
│   ├── test_auth.py
│   └── test_tasks.py
├── alembic.ini
├── requirements.txt
└── README.md
```

## License

MIT
