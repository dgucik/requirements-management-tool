# Backend

Django and Django REST Framework backend for the Requirements Management Tool.

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env
uv run python manage.py migrate
uv run python manage.py runserver
```

The server runs at <http://127.0.0.1:8000/>. The admin site is available at
<http://127.0.0.1:8000/admin/>.

## Authentication

The API uses JWT authentication. Obtain a token pair with:

```http
POST /api/auth/token/
Content-Type: application/json

{"username": "your-username", "password": "your-password"}
```

Use the returned access token for protected endpoints:

```text
Authorization: Bearer <access-token>
```

Refresh an expired access token with `POST /api/auth/token/refresh/` and the refresh token.

## Tests

Install the project and development dependencies, then run:

```bash
uv sync
uv run pytest
```

To run only the project service tests:

```bash
uv run pytest apps/project/tests/services/test_project_create.py
```

## Configuration

Copy `.env.example` to `.env` and adjust the values for your environment. Settings are split into
thematic modules in `config/settings/` and exposed through `config.settings`:

- `environment.py`: `.env` loading and environment-dependent settings
- `database.py`: SQLite/PostgreSQL configuration
- `installed_apps.py`: installed Django applications
- `localization.py`, `static_files.py`: language, time zone and static files
- `middleware.py`, `templates.py`, `rest_framework.py`: framework-specific settings

For production, set a secure `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, configure
`DJANGO_ALLOWED_HOSTS`, and use a production database and static-file storage. Set
`DJANGO_DB_ENGINE=postgresql` and the PostgreSQL variables from `.env.example` to use PostgreSQL.
Leave `DJANGO_DB_ENGINE=sqlite` to use SQLite. Never commit `.env`.
