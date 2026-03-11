# API Reference — AI Recruiter Engine

**Base URL:** `/api/v1/`

---

## Vacancy Management

```
GET    /api/v1/vacancies/                # List vacancies
POST   /api/v1/vacancies/               # Create vacancy
GET    /api/v1/vacancies/{id}/          # Retrieve
PUT    /api/v1/vacancies/{id}/          # Update
PATCH  /api/v1/vacancies/{id}/          # Partial update
DELETE /api/v1/vacancies/{id}/          # Delete
```

## Job Advertisements

```
GET    /api/v1/job-ads/                  # List ads
POST   /api/v1/job-ads/                 # Create ad
GET    /api/v1/job-ads/{id}/            # Retrieve
PUT    /api/v1/job-ads/{id}/            # Update
DELETE /api/v1/job-ads/{id}/            # Delete
```

```
CRUD   /api/v1/job-ad-publications/     # Publication channels
```

## Candidate Management

```
GET    /api/v1/candidates/               # List candidates
POST   /api/v1/candidates/              # Ingest candidate
GET    /api/v1/candidates/{id}/         # Retrieve
PUT    /api/v1/candidates/{id}/         # Update
DELETE /api/v1/candidates/{id}/         # Delete
```

## Interview Management

```
GET    /api/v1/interviews/               # List interviews
POST   /api/v1/interviews/              # Schedule interview
GET    /api/v1/interviews/{id}/         # Retrieve
PUT    /api/v1/interviews/{id}/         # Update
DELETE /api/v1/interviews/{id}/         # Delete
```

## Interview Scheduling

```
CRUD   /api/v1/scheduling/              # Interviewer availability & calendar
```

## Interview Integrity

```
GET    /api/v1/integrity/                # List integrity signals/reports
POST   /api/v1/integrity/               # Report integrity signal
GET    /api/v1/integrity/{id}/          # Retrieve
```

## Hiring Decisions

```
GET    /api/v1/decisions/                # List decisions
POST   /api/v1/decisions/               # Record decision
GET    /api/v1/decisions/{id}/          # Retrieve
```

## Business Rules

```
CRUD   /api/v1/rules/                   # Hiring business rules
CRUD   /api/v1/rule-exceptions/         # Rule exceptions
```

## Internal Mobility

```
CRUD   /api/v1/mobility/                # Internal transfers
CRUD   /api/v1/succession/              # Succession plans
CRUD   /api/v1/promotion-cycles/        # Promotion cycles
CRUD   /api/v1/promotions/              # Individual promotions
```

---

## Recruitment Pipeline Flow

```
Vacancy → Job Ad → Candidate Ingestion → Screening
    → Interview Scheduling → Interview Execution
    → Integrity Monitoring → Feedback & Calibration
    → Hiring Decision → Offer (Employee Lifecycle)
```
