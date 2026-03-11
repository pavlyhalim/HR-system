import os
import sys
from datetime import timedelta
from pathlib import Path

import environ

# ──────────────────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Add apps/ to the Python path
sys.path.insert(0, str(BASE_DIR / "apps"))

# ──────────────────────────────────────────────────────────
# SECURITY
# ──────────────────────────────────────────────────────────
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# ──────────────────────────────────────────────────────────
# APPLICATION DEFINITION
# ──────────────────────────────────────────────────────────
DJANGO_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "django_extensions",
]

LOCAL_APPS = [
    "apps.core",
    "apps.accounts",
    "apps.job_description",
    "apps.recruiter",
    "apps.employee_lifecycle",
    "apps.oma",
    "apps.hr_strategy",
    "apps.tna",
    "apps.payroll",
    "apps.performance",
    "apps.notifications",
    "apps.documents",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ──────────────────────────────────────────────────────────
# MIDDLEWARE
# ──────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.audit.AuditLogMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ──────────────────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="hr-dashboard"),
        "USER": env("DB_USER", default="orange"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}

# ──────────────────────────────────────────────────────────
# AUTH
# ──────────────────────────────────────────────────────────
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ──────────────────────────────────────────────────────────
# INTERNATIONALIZATION
# ──────────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────────────────
# STATIC & MEDIA
# ──────────────────────────────────────────────────────────
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ──────────────────────────────────────────────────────────
# DJANGO REST FRAMEWORK
# ──────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
}

# ──────────────────────────────────────────────────────────
# SIMPLE JWT
# ──────────────────────────────────────────────────────────
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ──────────────────────────────────────────────────────────
# DRF-SPECTACULAR (SWAGGER / OPENAPI)
# ──────────────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE": "HR System API",
    "DESCRIPTION": (
        "**AI-Driven Human Resources Platform** — A comprehensive enterprise backend "
        "powering 8 intelligent HR engines.\n\n"
        "### Engines\n"
        "| Engine | Description |\n"
        "|--------|-------------|\n"
        "| **JD Generator** | AI-powered job description creation, versioning & benchmarking |\n"
        "| **AI Recruiter** | End-to-end recruitment — vacancies, candidates, interviews, integrity |\n"
        "| **Employee Lifecycle** | Offers → onboarding → probation → offboarding automation |\n"
        "| **OMA** | Organizational Maturity Assessment with gap/risk analysis |\n"
        "| **HR Strategy** | Strategic pillars, KPIs, roadmaps & confidence scoring |\n"
        "| **TNA** | Training Needs Analysis — skill gaps & learning paths |\n"
        "| **Payroll** | Salary structures, payroll cycles & payslip generation |\n"
        "| **Performance** | Review cycles, goal cascades, calibrations & bias detection |\n\n"
        "### Authentication\n"
        "All endpoints require **JWT Bearer** tokens. Obtain one via `POST /api/v1/auth/login/` "
        "with your email and password, then click **Authorize** above.\n"
    ),
    "VERSION": "1.0.0",
    "CONTACT": {
        "name": "HR System Engineering",
        "email": "admin@hr-system.com",
    },
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": False,
        "filter": True,
        "syntaxHighlight.theme": "monokai",
        "docExpansion": "list",
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
        "tryItOutEnabled": True,
        "requestSnippetsEnabled": True,
    },
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_UI_SETTINGS": {
        "theme": {
            "colors": {
                "primary": {"main": "#6c63ff"},
            },
            "typography": {
                "fontFamily": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                "headings": {"fontFamily": "Inter, sans-serif"},
                "code": {"fontFamily": "JetBrains Mono, Fira Code, Consolas, monospace"},
            },
            "sidebar": {
                "backgroundColor": "#161922",
                "textColor": "#9ca3b4",
                "activeTextColor": "#6c63ff",
            },
            "rightPanel": {
                "backgroundColor": "#0f1117",
            },
        },
        "hideDownloadButton": False,
        "expandResponses": "200",
        "pathInMiddlePanel": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "ENUM_NAME_OVERRIDES": {},
    "SCHEMA_PATH_PREFIX": "/api/v[0-9]",
    "SORT_OPERATIONS": True,
    "TAGS": [
        {"name": "Auth", "description": "Authentication, registration, JWT token management & user profiles"},
        {"name": "Job Descriptions", "description": "AI-powered JD generation, versioning, competency mapping & approval workflows"},
        {"name": "Vacancies", "description": "Job vacancy creation, publishing & analytics tracking"},
        {"name": "Candidates", "description": "Candidate ingestion, scoring, communication logs & consent management"},
        {"name": "Interviews", "description": "Interview scheduling, questions, responses, feedback & calibration"},
        {"name": "Integrity", "description": "AI interview integrity monitoring — signals, reports & baselines"},
        {"name": "Decisions", "description": "Hiring decisions, business rules & rule exception management"},
        {"name": "Mobility", "description": "Internal mobility tracking & lateral movement management"},
        {"name": "Succession", "description": "Succession planning & leadership pipeline management"},
        {"name": "Promotions", "description": "Promotion cycles, individual promotions & approval tracking"},
        {"name": "Employee Lifecycle", "description": "Full lifecycle — preboarding, offers, contracts, onboarding, probation, offboarding & settlements"},
        {"name": "OMA", "description": "Organizational Maturity Assessment — surveys, scoring, gap analysis, risks & roadmaps"},
        {"name": "HR Strategy", "description": "AI strategy engine — pillars, initiatives, KPIs, readiness, confidence & risk analysis"},
        {"name": "TNA", "description": "Training Needs Analysis — cycles, skill gaps, priorities & learning paths"},
        {"name": "Payroll", "description": "Payroll automation — salary structures, cycles, records, payslips, tax & bank files"},
        {"name": "Performance", "description": "Performance management — frameworks, reviews, goals, calibrations, ratings & bias detection"},
        {"name": "Notifications", "description": "Notification delivery & template management"},
        {"name": "Documents", "description": "Document storage, retrieval & access audit logging"},
    ],
}

# ──────────────────────────────────────────────────────────
# UNFOLD ADMIN
# ──────────────────────────────────────────────────────────
UNFOLD = {
    "SITE_TITLE": "HR System Admin",
    "SITE_HEADER": "HR System",
    "SITE_SYMBOL": "work",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Authentication",
                "items": [
                    {"title": "Users", "icon": "person", "link": "/admin/accounts/user/"},
                ],
            },
            {
                "title": "Job Descriptions",
                "items": [
                    {"title": "Job Analysis", "icon": "assignment", "link": "/admin/job_description/jobanalysisinput/"},
                    {"title": "Job Descriptions", "icon": "description", "link": "/admin/job_description/jobdescription/"},
                ],
            },
            {
                "title": "Recruitment",
                "items": [
                    {"title": "Vacancies", "icon": "work", "link": "/admin/recruiter/vacancy/"},
                    {"title": "Candidates", "icon": "people", "link": "/admin/recruiter/candidate/"},
                    {"title": "Interviews", "icon": "record_voice_over", "link": "/admin/recruiter/interview/"},
                    {"title": "Hiring Decisions", "icon": "gavel", "link": "/admin/recruiter/hiringdecision/"},
                ],
            },
            {
                "title": "Employee Lifecycle",
                "items": [
                    {"title": "Employees", "icon": "badge", "link": "/admin/employee_lifecycle/employee/"},
                    {"title": "Offers", "icon": "local_offer", "link": "/admin/employee_lifecycle/offer/"},
                    {"title": "Contracts", "icon": "handshake", "link": "/admin/employee_lifecycle/contract/"},
                ],
            },
            {
                "title": "OMA",
                "items": [
                    {"title": "Surveys", "icon": "poll", "link": "/admin/oma/omasurvey/"},
                    {"title": "Maturity Levels", "icon": "trending_up", "link": "/admin/oma/amamaturitylevel/"},
                ],
            },
            {
                "title": "HR Strategy",
                "items": [
                    {"title": "Strategies", "icon": "strategy", "link": "/admin/hr_strategy/hrstrategy/"},
                    {"title": "Pillars", "icon": "view_column", "link": "/admin/hr_strategy/strategicpillar/"},
                ],
            },
            {
                "title": "Other Engines",
                "items": [
                    {"title": "TNA Cycles", "icon": "school", "link": "/admin/tna/tnacycle/"},
                    {"title": "Payroll Cycles", "icon": "payments", "link": "/admin/payroll/payrollcycle/"},
                    {"title": "Performance Reviews", "icon": "assessment", "link": "/admin/performance/reviewcycle/"},
                ],
            },
        ],
    },
}

# ──────────────────────────────────────────────────────────
# CORS
# ──────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["http://localhost:3000"])

# ──────────────────────────────────────────────────────────
# CELERY
# ──────────────────────────────────────────────────────────
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# ──────────────────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
