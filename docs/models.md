# Data Model Reference

Complete reference for all 105+ models across 12 Django apps. All models inherit from `core.BaseModel` (UUID PK, timestamps, soft delete) unless noted.

---

## Core (`apps.core`)

### BaseModel *(abstract)*
| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `created_at` | DateTime | Auto-set on creation |
| `updated_at` | DateTime | Auto-set on save |
| `is_active` | Boolean | Soft delete flag (default: True) |

### AuditLog
| Field | Type | Description |
|-------|------|-------------|
| `user` | FK → User | Who performed the action |
| `action` | String | HTTP method (GET, POST, etc.) |
| `path` | String | Request URL path |
| `body` | JSON | Request body (for mutations) |
| `ip_address` | GenericIP | Client IP |
| `timestamp` | DateTime | When it happened |

### SystemConfiguration
| Field | Type | Description |
|-------|------|-------------|
| `key` | String | Configuration key (unique) |
| `value` | JSON | Configuration value |
| `description` | Text | Human-readable description |

---

## Accounts (`apps.accounts`)

### User
| Field | Type | Description |
|-------|------|-------------|
| `email` | Email | **USERNAME_FIELD** — unique, used for login |
| `first_name` | String | First name |
| `last_name` | String | Last name |
| `role` | Choice | One of 13 roles (see below) |
| `phone` | String | Phone number (optional) |
| `department` | String | Department (optional) |
| `is_staff` | Boolean | Admin access |
| `is_superuser` | Boolean | Full permissions |

**Roles:** `admin`, `hr`, `manager`, `employee`, `recruiter`, `candidate`, `interviewer`, `auditor`, `executive`, `strategy_owner`, `payroll`, `legal`, `it`

---

## Job Description Engine (`apps.job_description`)

### JobAnalysisInput
| Field | Type | Description |
|-------|------|-------------|
| `title` | String | Job title to analyze |
| `department` | String | Target department |
| `level` | String | Seniority level |
| `requirements` | Text | Raw requirements text |
| `created_by` | FK → User | Requester |

### JobDescription
| Field | Type | Description |
|-------|------|-------------|
| `analysis` | FK → JobAnalysisInput | Source analysis |
| `title` | String | JD title |
| `summary` | Text | Executive summary |
| `responsibilities` | JSON | List of responsibilities |
| `qualifications` | JSON | Required qualifications |
| `status` | Choice | draft / pending_approval / approved / rejected |
| `created_by` | FK → User | Author |
| `approved_by` | FK → User | Approver (nullable) |

### JobDescriptionVersion
| Field | Type | Description |
|-------|------|-------------|
| `job_description` | FK → JobDescription | Parent JD |
| `version_number` | Integer | Sequential version |
| `content` | JSON | Full version snapshot |
| `change_notes` | Text | What changed |

### JDCompetency
| Field | Type | Description |
|-------|------|-------------|
| `job_description` | FK → JobDescription | Parent JD |
| `name` | String | Competency name |
| `category` | String | Category (technical, soft, etc.) |
| `level` | String | Required proficiency level |
| `weight` | Decimal | Importance weight |

### JDBenchmarkResult
| Field | Type | Description |
|-------|------|-------------|
| `job_description` | FK → JobDescription | Benchmarked JD |
| `benchmark_source` | String | Source of benchmark data |
| `score` | Decimal | Benchmark score |
| `details` | JSON | Detailed comparison data |

### JDApprovalLog
| Field | Type | Description |
|-------|------|-------------|
| `job_description` | FK → JobDescription | JD being approved |
| `action` | Choice | submitted / approved / rejected |
| `user` | FK → User | Who took the action |
| `comment` | Text | Optional comment |

### JDConsumerReference
| Field | Type | Description |
|-------|------|-------------|
| `job_description` | FK → JobDescription | Referenced JD |
| `consumer_type` | String | What's using it (vacancy, posting, etc.) |
| `consumer_id` | UUID | ID of the consuming entity |

---

## Recruiter Engine (`apps.recruiter`)

### Vacancy
| Field | Type | Description |
|-------|------|-------------|
| `jd_id` | UUID | Link to Job Description |
| `title` | String | Position title |
| `department` | String | Department |
| `location` | String | Job location |
| `employment_type` | Choice | full_time / part_time / contract |
| `status` | Choice | open / closed / on_hold / cancelled |
| `positions_count` | Integer | Number of openings |
| `deadline` | Date | Application deadline |

### Candidate
| Field | Type | Description |
|-------|------|-------------|
| `first_name` | String | Candidate first name |
| `last_name` | String | Candidate last name |
| `email` | Email | Candidate email |
| `phone` | String | Phone number |
| `resume` | File | Uploaded resume |
| `source` | String | How they were sourced |
| `overall_score` | Decimal | AI-calculated score |
| `status` | Choice | new / screening / interview / offer / hired / rejected |

### Interview
| Field | Type | Description |
|-------|------|-------------|
| `candidate` | FK → Candidate | Interviewee |
| `vacancy` | FK → Vacancy | Position |
| `interview_type` | Choice | phone / video / in_person / panel |
| `scheduled_at` | DateTime | When it's scheduled |
| `duration_minutes` | Integer | Expected duration |
| `status` | Choice | scheduled / completed / cancelled / no_show |
| `location` | String | Physical/virtual location |

### InterviewIntegritySignal
| Field | Type | Description |
|-------|------|-------------|
| `interview` | FK → Interview | Monitored interview |
| `signal_type` | String | Type of integrity signal |
| `severity` | Choice | low / medium / high / critical |
| `details` | JSON | Signal details |
| `timestamp` | DateTime | When detected |

### HiringDecision
| Field | Type | Description |
|-------|------|-------------|
| `candidate` | FK → Candidate | Candidate |
| `vacancy` | FK → Vacancy | Position |
| `decision` | Choice | hire / reject / waitlist |
| `justification` | Text | Decision reasoning |
| `decided_by` | FK → User | Decision maker |

*Additional models:* `JobAdvertisement`, `JobAdPublication`, `JobAdAnalytics`, `CandidateVacancy`, `CandidateCommunicationLog`, `InterviewInterviewer`, `InterviewQuestion`, `InterviewResponse`, `InterviewFeedback`, `InterviewFeedbackCalibration`, `InterviewIntegrityReport`, `CandidateConsentRecord`, `IntegrityBaseline`, `IntegrityDataAccessLog`, `BusinessRule`, `RuleException`, `InterviewerProfile`, `InterviewerAvailability`, `InternalMobility`, `SuccessionPlan`, `PromotionCycle`, `Promotion`

---

## Employee Lifecycle (`apps.employee_lifecycle`)

### Employee
| Field | Type | Description |
|-------|------|-------------|
| `user` | FK → User | Linked user account |
| `employee_id` | String | Company employee ID |
| `department` | String | Department |
| `position` | String | Job title |
| `hire_date` | Date | Date of hire |
| `manager` | FK → User | Direct manager |
| `employment_type` | Choice | full_time / part_time / contract |
| `status` | Choice | preboarding / active / probation / offboarding / terminated |

### Offer
| Field | Type | Description |
|-------|------|-------------|
| `candidate` | FK (UUID) | Candidate reference |
| `template` | FK → OfferTemplate | Based on template |
| `position` | String | Offered position |
| `salary` | Decimal | Offered salary |
| `start_date` | Date | Proposed start date |
| `status` | Choice | draft / sent / accepted / rejected / expired |
| `valid_until` | Date | Offer expiration |

### Contract
| Field | Type | Description |
|-------|------|-------------|
| `employee` | FK → Employee | Employee |
| `contract_type` | Choice | permanent / fixed_term / probation |
| `start_date` | Date | Contract start |
| `end_date` | Date | Contract end (nullable for permanent) |
| `status` | Choice | draft / active / expired / terminated |

*Additional models:* `EmployeeLifecycleState`, `OfferTemplate`, `ContractVersion`, `ContractSignature`, `EmployeePersonalData`, `OnboardingChecklist`, `OnboardingTask`, `ProbationRecord`, `OffboardingRecord`, `FinalSettlement`, `ApprovalRequest`, `ApprovalAction`

---

## OMA Engine (`apps.oma`)

### OMASurvey
Creates maturity assessment surveys with configurable questions and scoring.

### OMADomainScore
Stores calculated scores per organizational domain after survey analysis.

### OMAGap / OMARisk
Identifies gaps between current and target maturity, with associated risk levels.

### OMARoadmap
AI-generated improvement roadmaps based on gap analysis.

*All 13 models:* `OMASurvey`, `OMASurveyQuestion`, `OMASurveyResponse`, `OMANormalizedData`, `OMADomainScore`, `OMAValidationResult`, `OMAMaturityLevel`, `OMAGap`, `OMARisk`, `OMARoadmap`, `OMABenchmark`, `OMABenchmarkDataset`, `OMAStrategyExport`

---

## HR Strategy Engine (`apps.hr_strategy`)

### HRStrategy
Top-level strategy document with version control.

### StrategicPillar
Major focus areas within a strategy (e.g., Talent Acquisition, Learning & Dev).

### StrategicInitiative
Specific projects/programs under a pillar with dependencies, timelines, and ownership.

### StrategyKPI
Key performance indicators linked to pillars/initiatives with target values.

*All 13 models:* `HRStrategy`, `StrategyVersion`, `StrategicPillar`, `StrategicInitiative`, `InitiativeDependency`, `StrategyKPI`, `StrategyRoadmap`, `StrategyReadinessScore`, `StrategyConfidenceLevel`, `StrategyBenchmark`, `StrategyExecutionLink`, `StrategyExplainability`, `StrategyRiskAnalysis`

---

## TNA Engine (`apps.tna`)

| Model | Purpose |
|-------|---------|
| `TNACycle` | Training needs assessment cycle |
| `SkillGapAnalysis` | Identified skill gaps per employee/department |
| `ManagerTNAInput` | Manager assessments of team training needs |
| `TrainingPriority` | Prioritized training recommendations |
| `LearningPath` | Recommended learning paths |
| `TNAReport` | Generated assessment reports |

---

## Payroll Engine (`apps.payroll`)

| Model | Purpose |
|-------|---------|
| `SalaryStructure` | Pay grades and compensation bands |
| `PayrollCycle` | Monthly/bi-weekly payroll runs |
| `PayrollRecord` | Individual employee payroll calculations |
| `Payslip` | Generated payslip documents |
| `TaxReport` | Tax filing reports |
| `BankFile` | Bank transfer file generation |

---

## Performance Engine (`apps.performance`)

| Model | Purpose |
|-------|---------|
| `PerformanceFramework` | Evaluation criteria and methodology |
| `ReviewCycle` | Periodic review cycles (annual, quarterly) |
| `GoalCascade` | Hierarchical goal setting (company → team → individual) |
| `PerformanceReview` | Individual performance reviews |
| `CalibrationSession` | Cross-team calibration sessions |
| `FinalRating` | Calibrated final ratings |
| `BiasDetectionResult` | AI bias detection in review patterns |

---

## Notifications (`apps.notifications`)

| Model | Purpose |
|-------|---------|
| `Notification` | Individual notification records (email, push, in-app) |
| `NotificationTemplate` | Reusable notification templates with variable substitution |

---

## Documents (`apps.documents`)

| Model | Purpose |
|-------|---------|
| `Document` | File metadata, storage, and categorization |
| `DocumentAccessLog` | Audit trail of who accessed which document |
