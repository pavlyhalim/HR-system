# API Reference — Job Description Engine

**Base URL:** `/api/v1/jd/`

---

## Endpoints

### Job Analysis Inputs

```
GET    /api/v1/jd/job-analysis/          # List all
POST   /api/v1/jd/job-analysis/          # Create new
GET    /api/v1/jd/job-analysis/{id}/     # Retrieve
PUT    /api/v1/jd/job-analysis/{id}/     # Full update
PATCH  /api/v1/jd/job-analysis/{id}/     # Partial update
DELETE /api/v1/jd/job-analysis/{id}/     # Delete
```

### Job Descriptions

```
GET    /api/v1/jd/job-descriptions/                    # List all
POST   /api/v1/jd/job-descriptions/                    # Create new
GET    /api/v1/jd/job-descriptions/{id}/               # Retrieve
PUT    /api/v1/jd/job-descriptions/{id}/               # Full update
PATCH  /api/v1/jd/job-descriptions/{id}/               # Partial update
DELETE /api/v1/jd/job-descriptions/{id}/               # Delete
```

**Custom Actions:**
```
POST   /api/v1/jd/job-descriptions/{id}/generate/        # AI-generate JD content
POST   /api/v1/jd/job-descriptions/{id}/submit_approval/ # Submit for approval
POST   /api/v1/jd/job-descriptions/{id}/approve/         # Approve JD
POST   /api/v1/jd/job-descriptions/{id}/reject/          # Reject JD
POST   /api/v1/jd/job-descriptions/{id}/create_version/  # Create new version
GET    /api/v1/jd/job-descriptions/{id}/list_versions/   # List all versions
GET    /api/v1/jd/job-descriptions/{id}/export/          # Export JD
POST   /api/v1/jd/job-descriptions/{id}/benchmark/       # Run benchmark
POST   /api/v1/jd/job-descriptions/{id}/validate_jd/     # Validate JD content
GET    /api/v1/jd/job-descriptions/{id}/approval_history/ # View approval history
```

### JD Competencies

```
GET    /api/v1/jd/jd-competencies/       # List all
POST   /api/v1/jd/jd-competencies/       # Create
GET    /api/v1/jd/jd-competencies/{id}/  # Retrieve
PUT    /api/v1/jd/jd-competencies/{id}/  # Update
DELETE /api/v1/jd/jd-competencies/{id}/  # Delete
```

### JD Consumer References

```
GET    /api/v1/jd/jd-consumers/          # List all (read-only)
GET    /api/v1/jd/jd-consumers/{id}/     # Retrieve
```

---

## Workflow

```
1. Create JobAnalysisInput → raw requirements
2. Create JobDescription (or use /generate/ action)
3. Add JDCompetency entries
4. Submit for approval → /submit_approval/
5. Approve/Reject → /approve/ or /reject/
6. Create versions for iterations → /create_version/
7. Benchmark against industry → /benchmark/
8. Link to Vacancy via JDConsumerReference
```
