# API Reference — OMA, HR Strategy, TNA, Payroll, Performance, Notifications & Documents

---

## OMA — Organizational Maturity Assessment

**Base URL:** `/api/v1/oma/`

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/surveys/` | CRUD | Maturity assessment surveys |
| `/questions/` | CRUD | Survey questions |
| `/responses/` | CRUD | Survey responses |
| `/normalization/` | CRUD | Normalized data processing |
| `/domain-scores/` | CRUD | Calculated domain scores |
| `/validation/` | CRUD | Validation results |
| `/maturity/` | CRUD | Maturity level classifications |
| `/gaps/` | CRUD | Identified maturity gaps |
| `/risks/` | CRUD | Risk assessments |
| `/roadmaps/` | CRUD | Improvement roadmaps |
| `/benchmarks/` | CRUD | Benchmark comparisons |
| `/benchmark-datasets/` | CRUD | Benchmark reference datasets |
| `/strategy-exports/` | CRUD | Strategy integration exports |

---

## HR Strategy Engine

**Base URL:** `/api/v1/strategy/`

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/strategies/` | CRUD | Top-level HR strategies |
| `/versions/` | CRUD | Strategy version history |
| `/pillars/` | CRUD | Strategic pillars/focus areas |
| `/initiatives/` | CRUD | Strategic initiatives |
| `/dependencies/` | CRUD | Initiative dependencies |
| `/kpis/` | CRUD | Key performance indicators |
| `/roadmaps/` | CRUD | Strategy roadmaps |
| `/readiness/` | CRUD | Readiness scores |
| `/confidence/` | CRUD | Confidence levels |
| `/benchmarks/` | CRUD | Strategy benchmarks |
| `/explainability/` | CRUD | AI explainability reports |
| `/risks/` | CRUD | Strategy risk analysis |

---

## TNA — Training Needs Analysis

**Base URL:** `/api/v1/tna/`

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/cycles/` | CRUD | TNA assessment cycles |
| `/skill-gaps/` | CRUD | Skill gap analyses |
| `/manager-inputs/` | CRUD | Manager training assessments |
| `/priorities/` | CRUD | Training priorities |
| `/learning-paths/` | CRUD | Recommended learning paths |
| `/reports/` | CRUD | TNA reports |

---

## Payroll Automation

**Base URL:** `/api/v1/payroll/`

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/salary-structures/` | CRUD | Pay grades and bands |
| `/cycles/` | CRUD | Payroll run cycles |
| `/records/` | CRUD | Individual payroll records |
| `/payslips/` | CRUD | Generated payslips |
| `/tax-reports/` | CRUD | Tax filing reports |
| `/bank-files/` | CRUD | Bank transfer files |

---

## Performance Management

**Base URL:** `/api/v1/performance/`

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/frameworks/` | CRUD | Evaluation frameworks |
| `/cycles/` | CRUD | Review cycles |
| `/goals/` | CRUD | Goal cascades |
| `/reviews/` | CRUD | Performance reviews |
| `/calibrations/` | CRUD | Calibration sessions |
| `/ratings/` | CRUD | Final ratings |

---

## Notifications

**Base URL:** `/api/v1/notifications/`

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/notifications/` | CRUD | Notification records |
| `/templates/` | CRUD | Notification templates |

---

## Documents

**Base URL:** `/api/v1/documents/`

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/documents/` | CRUD | Document management |
| `/documents/{id}/access_log/` | GET | View access logs for a document |
| `/documents/{id}/log_access/` | POST | Log a document access event |
| `/access-logs/` | GET | All access logs (read-only) |

---

## Common Parameters (All Endpoints)

| Parameter | Type | Description |
|-----------|------|-------------|
| `?page=N` | Integer | Page number (default: 1) |
| `?page_size=N` | Integer | Results per page (default: 20) |
| `?search=term` | String | Full-text search |
| `?ordering=field` | String | Sort by field (prefix `-` for descending) |

## Standard Response Format

**List Response:**
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/v1/.../&page=2",
  "previous": null,
  "results": [...]
}
```

**Error Response:**
```json
{
  "detail": "Error message",
  "code": "error_code"
}
```

**Validation Error:**
```json
{
  "field_name": ["Error message for this field"]
}
```
