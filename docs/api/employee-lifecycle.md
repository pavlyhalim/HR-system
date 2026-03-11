# API Reference — Employee Lifecycle Engine

**Base URL:** `/api/v1/lifecycle/`

---

## Endpoints

### Employees
```
GET    /api/v1/lifecycle/employees/                    # List
POST   /api/v1/lifecycle/employees/                   # Create
GET    /api/v1/lifecycle/employees/{id}/              # Retrieve
PUT    /api/v1/lifecycle/employees/{id}/              # Update
PATCH  /api/v1/lifecycle/employees/{id}/              # Partial update
DELETE /api/v1/lifecycle/employees/{id}/              # Delete
POST   /api/v1/lifecycle/employees/{id}/lifecycle/    # Get lifecycle state
POST   /api/v1/lifecycle/employees/{id}/transition/   # Transition state
```

### Preboarding
```
POST   /api/v1/lifecycle/preboarding/initiate/        # Start preboarding
GET    /api/v1/lifecycle/preboarding/preboarding_status/ # Check status
POST   /api/v1/lifecycle/preboarding/complete/        # Mark complete
```

### Offers
```
CRUD   /api/v1/lifecycle/offer-templates/             # Offer templates
CRUD   /api/v1/lifecycle/offers/                      # Offers
POST   /api/v1/lifecycle/offers/{id}/submit_approval/ # Submit for approval
POST   /api/v1/lifecycle/offers/{id}/approve/         # Approve
POST   /api/v1/lifecycle/offers/{id}/reject/          # Reject
POST   /api/v1/lifecycle/offers/{id}/send_offer/      # Send to candidate
```

### Contracts
```
CRUD   /api/v1/lifecycle/contracts/                   # Contracts
POST   /api/v1/lifecycle/contracts/{id}/submit_approval/ # Submit
POST   /api/v1/lifecycle/contracts/{id}/approve/      # Approve
POST   /api/v1/lifecycle/contracts/{id}/send_signature/ # Send for e-signature
POST   /api/v1/lifecycle/contracts/{id}/sign/         # Record signature
GET    /api/v1/lifecycle/contracts/{id}/versions/     # Version history
```

### Onboarding
```
CRUD   /api/v1/lifecycle/onboarding/                  # Checklists
CRUD   /api/v1/lifecycle/onboarding-tasks/            # Individual tasks
POST   /api/v1/lifecycle/onboarding/{id}/initiate/    # Start onboarding
GET    /api/v1/lifecycle/onboarding/{id}/checklist/   # Get checklist
POST   /api/v1/lifecycle/onboarding/{id}/complete_task/ # Complete a task
```

### Probation
```
CRUD   /api/v1/lifecycle/probation/                   # Probation records
POST   /api/v1/lifecycle/probation/{id}/review/       # Submit review
POST   /api/v1/lifecycle/probation/{id}/confirm/      # Confirm/extend
```

### Offboarding
```
CRUD   /api/v1/lifecycle/offboarding/                 # Offboarding records
POST   /api/v1/lifecycle/offboarding/{id}/initiate/   # Start offboarding
POST   /api/v1/lifecycle/offboarding/{id}/complete/   # Complete offboarding
```

### Settlements & Personal Data
```
CRUD   /api/v1/lifecycle/settlements/                 # Final settlements
CRUD   /api/v1/lifecycle/personal-data/               # Employee personal data
```

### Approvals
```
CRUD   /api/v1/lifecycle/approvals/                   # Approval requests
```

---

## Lifecycle Flow

```
Hired → Preboarding → Offer → Contract → Onboarding
    → Active → Probation Review → Confirmed
    → [Offboarding] → Final Settlement → Terminated
```
