# Architecture & Design Decisions

## Overview

The HR System is a modular Django REST API backend designed around **8 independent HR engines**, each encapsulated in its own Django app. A shared `core` app provides common infrastructure (base models, pagination, audit logging, exception handling).

---

## High-Level Architecture

```
                    ┌─────────────┐
                    │   Clients   │
                    │ (SPA/Mobile)│
                    └──────┬──────┘
                           │ JWT Bearer Tokens
                    ┌──────▼──────┐
                    │   Nginx /   │
                    │   Gunicorn  │
                    └──────┬──────┘
                           │
          ┌────────────────▼────────────────┐
          │         Django + DRF            │
          │     config/settings/base.py     │
          ├─────────────────────────────────┤
          │  ┌─────────┐  ┌─────────────┐  │
          │  │  Auth    │  │ JD Generator│  │
          │  │ (JWT)    │  │   Engine    │  │
          │  ├─────────┤  ├─────────────┤  │
          │  │Recruiter │  │  Lifecycle  │  │
          │  │ Engine   │  │   Engine    │  │
          │  ├─────────┤  ├─────────────┤  │
          │  │  OMA     │  │  Strategy   │  │
          │  │ Engine   │  │   Engine    │  │
          │  ├─────────┤  ├─────────────┤  │
          │  │  TNA     │  │  Payroll    │  │
          │  │ Engine   │  │   Engine    │  │
          │  ├─────────┤  ├─────────────┤  │
          │  │Perform.  │  │ Notif/Docs  │  │
          │  │ Engine   │  │  Services   │  │
          │  └─────────┘  └─────────────┘  │
          ├─────────────────────────────────┤
          │          Core App              │
          │  BaseModel · AuditLog · Paging │
          └────────────┬────────────────────┘
                       │
          ┌────────────▼────────────────┐
          │     PostgreSQL (hr-dashboard)│
          └─────────────────────────────┘
                       │
          ┌────────────▼────────────────┐
          │     Redis (Celery Broker)    │
          └─────────────────────────────┘
```

---

## Design Principles

### 1. Domain-Driven App Separation

Each HR engine is a self-contained Django app with its own:
- Models (data layer)
- Serializers (validation + transformation)
- Views (API endpoints)
- URLs (routing)
- Tests (unit + integration)
- Services directory (business logic — placeholder for AI/ML integration)

This enables:
- Independent development and testing per engine
- Clear ownership boundaries
- Easy feature toggling (remove from `INSTALLED_APPS`)

### 2. BaseModel Pattern

All models inherit from `core.BaseModel`:

```python
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
```

**Benefits:**
- **UUID PKs** — No sequential ID enumeration, safe for public APIs
- **Timestamps** — Automatic audit trail on every record
- **Soft delete** — `is_active=False` instead of `DELETE` — data preservation for compliance
- **Consistent ordering** — Newest first by default, prevents pagination warnings

### 3. Split Settings

```
config/settings/
├── base.py          # All shared configuration
├── development.py   # DEBUG=True, sidecar assets, relaxed security
└── production.py    # DEBUG=False, strict security, external asset CDNs
```

Controlled via `DJANGO_SETTINGS_MODULE`:
- Dev: `config.settings.development`
- Prod: `config.settings.production`

### 4. JWT Authentication (Email-Based)

```python
AUTH_USER_MODEL = "accounts.User"
# User model: USERNAME_FIELD = "email"
```

- Login with `email` + `password` (not username)
- Access tokens: 30 minutes (short-lived for security)
- Refresh tokens: 7 days (rotated on use, old tokens blacklisted)
- `SessionAuthentication` also enabled for admin/browser access

### 5. Audit Logging

The `AuditLogMiddleware` in `core` records:
- User performing the action
- HTTP method and path
- Request body (for POST/PUT/PATCH)
- Timestamp

Stored in `core.AuditLog` model — queryable for compliance reporting.

### 6. API Versioning

All endpoints use URL prefix versioning: `/api/v1/`

This allows future `/api/v2/` without breaking existing clients.

### 7. Pagination

Standard cursor-based pagination via `core.pagination.StandardPagination`:
- Default page size: 20
- Configurable per-request with `?page_size=N`

### 8. Throttling

```python
"DEFAULT_THROTTLE_RATES": {
    "anon": "100/hour",      # Unauthenticated users
    "user": "1000/hour",     # Authenticated users
}
```

---

## Data Flow Example: Recruitment Pipeline

```
1. POST /api/v1/jd/job-analysis/          → Create job analysis input
2. POST /api/v1/jd/job-descriptions/      → Generate JD from analysis
3. POST /api/v1/jd/job-descriptions/{id}/approve/  → Approve JD
4. POST /api/v1/vacancies/                → Create vacancy linked to JD
5. POST /api/v1/candidates/               → Ingest candidate
6. POST /api/v1/interviews/               → Schedule interview
7. POST /api/v1/integrity/                → Monitor interview integrity
8. POST /api/v1/decisions/                → Record hiring decision
9. POST /api/v1/lifecycle/offers/         → Generate offer
10. POST /api/v1/lifecycle/onboarding/    → Initiate onboarding
```

---

## Security Measures

| Measure | Implementation |
|---------|---------------|
| Authentication | JWT Bearer tokens (short-lived) |
| Authorization | DRF permission classes (IsAuthenticated default) |
| CORS | Explicit whitelist via `CORS_ALLOWED_ORIGINS` |
| CSRF | Enabled for session-based requests |
| Rate Limiting | 100/hr anonymous, 1000/hr authenticated |
| Input Validation | DRF serializer validation on all inputs |
| SQL Injection | Django ORM parameterized queries |
| XSS | Django template auto-escaping |
| Clickjacking | X-Frame-Options middleware |
| UUID PKs | Non-enumerable resource identifiers |
| Audit Trail | All mutations logged to AuditLog |

---

## Technology Choices

| Choice | Alternatives Considered | Rationale |
|--------|------------------------|-----------|
| Django + DRF | FastAPI, Flask | Mature ORM, admin, auth, migrations out of the box |
| PostgreSQL | MySQL, SQLite | JSON fields, UUID support, advanced indexing |
| JWT (simplejwt) | Session auth, OAuth2 | Stateless, works with SPA/mobile clients |
| drf-spectacular | drf-yasg | Better maintained, OpenAPI 3.0 native |
| django-unfold | Grappelli, Jazzmin | Modern UI, actively maintained, Material icons |
| Celery + Redis | Django-Q, Dramatiq | Industry standard, battle-tested at scale |
| django-environ | python-decouple | Django-specific, cleaner API |
