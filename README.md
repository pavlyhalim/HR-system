<p align="center">
  <img src="https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-3.15-ff1709?style=for-the-badge&logo=django&logoColor=white" alt="DRF">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/Celery-5.4-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery">
  <img src="https://img.shields.io/badge/Redis-5.0-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
</p>

# HR System — AI-Driven Human Resources Platform

A production-ready Django REST API backend powering **8 intelligent HR engines** with **105+ models**, **90+ API endpoints**, JWT authentication, and a custom dark-themed Swagger UI.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [HR Engines](#hr-engines)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Running Tests](#running-tests)
- [Admin Panel](#admin-panel)
- [Celery & Background Tasks](#celery--background-tasks)

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        CLIENT APPLICATIONS                       │
│              (React / Next.js / Mobile / Integrations)           │
└────────────────────────────┬─────────────────────────────────────┘
                             │  HTTPS + JWT Bearer
┌────────────────────────────▼─────────────────────────────────────┐
│                      DJANGO REST FRAMEWORK                       │
│                        /api/v1/ prefix                           │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│   Auth   │    JD    │Recruiter │Lifecycle │   OMA    │ Strategy │
│  Engine  │Generator │  Engine  │  Engine  │  Engine  │  Engine  │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│   TNA    │ Payroll  │Perform.  │  Notif.  │  Docs    │   Core   │
│  Engine  │  Engine  │  Engine  │ Service  │ Service  │ (Shared) │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────┤
│                     PostgreSQL  +  Redis                         │
└──────────────────────────────────────────────────────────────────┘
```

---

## HR Engines

| # | Engine | App | Models | Key Features |
|---|--------|-----|--------|-------------|
| 1 | **JD Generator** | `job_description` | 7 | AI-powered job description creation, versioning, competency mapping, benchmarking, approval workflows |
| 2 | **AI Recruiter** | `recruiter` | 27 | Vacancies, candidates, interviews, integrity monitoring, hiring decisions, business rules, internal mobility, succession planning, promotions |
| 3 | **Employee Lifecycle** | `employee_lifecycle` | 15 | Offers, contracts, onboarding checklists, probation tracking, offboarding, final settlements, approval chains |
| 4 | **OMA** | `oma` | 13 | Organizational maturity surveys, domain scoring, gap analysis, risk assessment, roadmaps, benchmarking |
| 5 | **HR Strategy** | `hr_strategy` | 13 | Strategic pillars, initiatives, KPIs, roadmaps, readiness scores, confidence levels, risk analysis |
| 6 | **TNA** | `tna` | 6 | Training needs cycles, skill gap analysis, manager inputs, learning paths, reports |
| 7 | **Payroll** | `payroll` | 6 | Salary structures, payroll cycles, records, payslips, tax reports, bank files |
| 8 | **Performance** | `performance` | 7 | Frameworks, review cycles, goal cascades, calibration sessions, bias detection, final ratings |

**Supporting services:** `accounts` (auth), `notifications`, `documents`, `core` (shared base models, audit log, pagination)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | Django 5.1 + Django REST Framework 3.15 |
| **Database** | PostgreSQL 16 |
| **Auth** | JWT via `djangorestframework-simplejwt` (email-based login) |
| **Admin** | [django-unfold](https://github.com/unfoldadmin/django-unfold) (modern admin UI) |
| **API Docs** | [drf-spectacular](https://github.com/tfranzel/drf-spectacular) — Swagger UI + ReDoc (custom dark theme) |
| **Task Queue** | Celery 5.4 + Redis |
| **Filtering** | django-filter + DRF SearchFilter + OrderingFilter |
| **CORS** | django-cors-headers |
| **Config** | django-environ (`.env` based) |

---

## Project Structure

```
HR-system/
├── config/                     # Django project configuration
│   ├── settings/
│   │   ├── base.py             # Shared settings (DRF, JWT, Swagger, DB, etc.)
│   │   ├── development.py      # Dev overrides (DEBUG, sidecar)
│   │   └── production.py       # Production overrides
│   ├── urls.py                 # Root URL routing (/api/v1/*)
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py               # Celery app configuration
│
├── apps/                       # All Django applications
│   ├── core/                   # Shared: BaseModel, AuditLog, pagination, exceptions, middleware
│   ├── accounts/               # User auth (JWT), registration, profiles, roles
│   ├── job_description/        # JD Generator engine
│   ├── recruiter/              # AI Recruiter engine (vacancies → hiring)
│   ├── employee_lifecycle/     # Employee lifecycle automation
│   ├── oma/                    # Organizational Maturity Assessment
│   ├── hr_strategy/            # AI HR Strategy engine
│   ├── tna/                    # Training Needs Analysis
│   ├── payroll/                # Payroll automation
│   ├── performance/            # Performance management
│   ├── notifications/          # Notification service
│   └── documents/              # Document & media service
│
├── templates/
│   └── drf_spectacular/        # Custom Swagger UI & ReDoc templates (dark theme)
│
├── client_docs/                # Original client requirement documents (PDFs)
├── docs/                       # Project documentation
│   ├── api/                    # API reference docs per engine
│   ├── setup.md                # Setup & installation guide
│   ├── architecture.md         # Architecture & design decisions
│   ├── models.md               # Complete data model reference
│   └── deployment.md           # Deployment guide
│
├── .env.example                # Environment variable template
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

Each app follows a consistent internal structure:
```
apps/<app_name>/
├── models/
│   ├── __init__.py
│   └── models.py          # All model definitions
├── views/
│   ├── __init__.py
│   └── views.py           # ViewSets and API views
├── serializers/
│   ├── __init__.py
│   └── serializers.py     # DRF serializers
├── tests/
│   ├── __init__.py
│   └── test_*.py          # Unit & integration tests
├── services/              # Business logic layer (placeholder)
├── admin.py               # Unfold admin registrations
├── urls.py                # Router + URL patterns
├── apps.py
└── migrations/
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis (for Celery — optional for dev)

### 1. Clone & Install Dependencies

```bash
git clone <repository-url>
cd HR-system
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

### 3. Create Database

```sql
-- In psql:
CREATE DATABASE "hr-dashboard";
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Start Development Server

```bash
python manage.py runserver
```

Visit:
| URL | Description |
|-----|------------|
| `http://localhost:8000/api/docs/` | **Swagger UI** (interactive API docs) |
| `http://localhost:8000/api/redoc/` | **ReDoc** (reference documentation) |
| `http://localhost:8000/admin/` | **Admin Panel** (django-unfold) |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | *required* |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `DB_NAME` | PostgreSQL database name | `hr-dashboard` |
| `DB_USER` | Database username | `orange` |
| `DB_PASSWORD` | Database password | *required* |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `CELERY_BROKER_URL` | Celery broker URL | `redis://localhost:6379/0` |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |

---

## API Documentation

### Interactive Docs

The API is fully documented with OpenAPI 3.0. Both Swagger and ReDoc feature a **custom dark-themed UI** with branded navigation.

- **Swagger UI** → `http://localhost:8000/api/docs/` — Interactive testing with "Try it out"
- **ReDoc** → `http://localhost:8000/api/redoc/` — Clean reference documentation
- **Raw Schema** → `http://localhost:8000/api/schema/` — OpenAPI JSON

### API Prefix

All API endpoints live under `/api/v1/`:

| Prefix | Engine |
|--------|--------|
| `/api/v1/auth/` | Authentication (login, register, profile, tokens) |
| `/api/v1/jd/` | Job Description Generator |
| `/api/v1/vacancies/` | Vacancy Management |
| `/api/v1/candidates/` | Candidate Management |
| `/api/v1/interviews/` | Interview Management |
| `/api/v1/lifecycle/` | Employee Lifecycle |
| `/api/v1/oma/` | Organizational Maturity Assessment |
| `/api/v1/strategy/` | HR Strategy Engine |
| `/api/v1/tna/` | Training Needs Analysis |
| `/api/v1/payroll/` | Payroll Automation |
| `/api/v1/performance/` | Performance Management |
| `/api/v1/notifications/` | Notifications |
| `/api/v1/documents/` | Documents |

---

## Authentication

The API uses **JWT (JSON Web Token)** authentication with email-based login.

### Login & Get Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hr-system.com", "password": "your-password"}'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1Qi...",
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

### Use Token

```bash
curl -H "Authorization: Bearer <access_token>" \
  http://localhost:8000/api/v1/lifecycle/employees/
```

### Token Lifetimes

| Token | Lifetime |
|-------|----------|
| Access | 30 minutes |
| Refresh | 7 days |

Refresh tokens are rotated on use and old tokens are blacklisted.

---

## Running Tests

```bash
# Run full test suite (76 tests)
python manage.py test

# Run with verbosity
python manage.py test --verbosity=2

# Run specific app tests
python manage.py test apps.accounts
python manage.py test apps.recruiter
python manage.py test apps.job_description
python manage.py test apps.employee_lifecycle

# Run all engine integration tests
python manage.py test apps.core.tests.test_all_engines
```

---

## Admin Panel

The admin panel uses **django-unfold** for a modern, responsive UI. Access it at `/admin/` with your superuser credentials.

Features:
- Custom sidebar navigation grouped by HR engine
- Material Design icons
- Search across all models
- Full CRUD for all 105+ models

---

## Celery & Background Tasks

Celery is configured for asynchronous task processing.

```bash
# Start worker
celery -A config worker -l info

# Start beat scheduler
celery -A config beat -l info
```

Configuration:
- **Broker**: Redis (default `redis://localhost:6379/0`)
- **Serializer**: JSON
- **Timezone**: UTC

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| **UUID Primary Keys** | Prevents enumeration attacks, safe for distributed systems |
| **Soft Delete** | `is_active` flag on BaseModel — data is never truly deleted |
| **Split Settings** | `base.py` / `development.py` / `production.py` for env-specific config |
| **Email Auth** | `USERNAME_FIELD = "email"` — industry standard for enterprise apps |
| **Audit Logging** | AuditLog middleware tracks all state-changing API calls |
| **drf-spectacular** | OpenAPI 3.0 schema generation over drf-yasg (better maintained, more features) |
| **django-unfold** | Modern admin over default Django admin |

---

## License

This project is proprietary. All rights reserved.
