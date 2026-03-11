# API Reference — Authentication

**Base URL:** `/api/v1/auth/`

---

## Endpoints

### Register New User

```
POST /api/v1/auth/register/
```

**Permission:** AllowAny

**Request Body:**
```json
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "role": "employee"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "employee"
}
```

---

### Login (Obtain JWT)

```
POST /api/v1/auth/login/
```

**Permission:** AllowAny

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1Qi...",
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

---

### Refresh Token

```
POST /api/v1/auth/token/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1Qi...",
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

> Refresh tokens rotate on use. The old refresh token is blacklisted.

---

### Get/Update Profile

```
GET  /api/v1/auth/profile/
PUT  /api/v1/auth/profile/
```

**Permission:** IsAuthenticated

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "employee",
  "phone": "+1234567890",
  "department": "Engineering"
}
```

---

### Change Password

```
POST /api/v1/auth/change-password/
```

**Permission:** IsAuthenticated

**Request Body:**
```json
{
  "old_password": "OldPass123!",
  "new_password": "NewPass456!"
}
```

---

### List Users

```
GET /api/v1/auth/users/
```

**Permission:** IsAuthenticated

**Query Parameters:** `?search=`, `?ordering=`, `?page=`

---

## User Roles

| Role | Value | Description |
|------|-------|-------------|
| Admin | `admin` | Full system access |
| HR | `hr` | HR operations |
| Manager | `manager` | Team management |
| Employee | `employee` | Self-service access |
| Recruiter | `recruiter` | Recruitment operations |
| Candidate | `candidate` | Candidate portal |
| Interviewer | `interviewer` | Interview panel |
| Auditor | `auditor` | Read-only audit access |
| Executive | `executive` | Executive dashboards |
| Strategy Owner | `strategy_owner` | Strategy management |
| Payroll | `payroll` | Payroll operations |
| Legal | `legal` | Legal/compliance |
| IT | `it` | IT administration |
