# Setup & Installation Guide

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11+ | Tested with 3.12 |
| PostgreSQL | 14+ | 16 recommended |
| Redis | 6+ | Required for Celery (optional in dev) |
| Git | 2.0+ | For version control |

---

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd HR-system
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Packages installed:**

| Package | Purpose |
|---------|---------|
| `django>=5.1` | Web framework |
| `djangorestframework>=3.15` | REST API framework |
| `djangorestframework-simplejwt>=5.3` | JWT authentication |
| `django-unfold>=0.83` | Modern admin panel |
| `drf-spectacular>=0.29` | OpenAPI 3.0 schema + Swagger/ReDoc |
| `django-cors-headers>=4.6` | CORS support |
| `django-filter>=25.0` | Queryset filtering |
| `django-environ>=0.13` | Environment variable management |
| `django-extensions>=4.1` | Development utilities |
| `psycopg2-binary>=2.9` | PostgreSQL adapter |
| `celery>=5.4` | Async task queue |
| `redis>=5.0` | Redis client (Celery broker) |

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and set these values:

```ini
DEBUG=True
SECRET_KEY=your-secret-key-here          # Generate a strong random key
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=hr-dashboard
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

> **Tip:** Generate a secure secret key with:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Create PostgreSQL Database

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create the database
CREATE DATABASE "hr-dashboard";

-- (Optional) Create a dedicated user
CREATE USER hr_admin WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE "hr-dashboard" TO hr_admin;
```

### 6. Run Database Migrations

```bash
python manage.py migrate
```

This applies ~30 migration files across all 12 apps.

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- **Email** (this is the USERNAME_FIELD)
- **First name**
- **Last name**
- **Password**

### 8. Verify Installation

```bash
# System check
python manage.py check

# Start dev server
python manage.py runserver
```

### 9. Verify Endpoints

| URL | Expected |
|-----|----------|
| http://localhost:8000/api/docs/ | Swagger UI with dark theme |
| http://localhost:8000/api/redoc/ | ReDoc documentation |
| http://localhost:8000/admin/ | Unfold admin panel |
| http://localhost:8000/api/schema/ | Raw OpenAPI schema |

---

## Running Tests

```bash
# Full suite
python manage.py test

# Verbose output
python manage.py test --verbosity=2

# Single app
python manage.py test apps.accounts
python manage.py test apps.recruiter
```

---

## Starting Celery (Optional)

```bash
# Terminal 1: Worker
celery -A config worker -l info

# Terminal 2: Beat scheduler
celery -A config beat -l info
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: psycopg2` | `pip install psycopg2-binary` |
| `FATAL: database "hr-dashboard" does not exist` | Create it: `CREATE DATABASE "hr-dashboard";` |
| `django.db.utils.OperationalError: connection refused` | Ensure PostgreSQL is running on port 5432 |
| `ConnectionError: Redis` | Install/start Redis or disable Celery for dev |
| `TemplateDoesNotExist: drf_spectacular/swagger_ui.html` | Ensure `templates/` dir is in project root |
