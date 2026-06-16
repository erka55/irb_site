# IRB API Specification
Version: 0.1

---

# 1. Base URL

/api/v1

---

# 2. Authentication

POST /auth/login
POST /auth/logout
POST /auth/refresh

---

# 3. Users

GET /users
GET /users/{id}
POST /users
PUT /users/{id}
DELETE /users/{id}

---

# 4. Protocols

## Create Protocol

POST /protocols

Request:
```json
{
  "title": "Study on...",
  "abstract": "...",
  "pi_id": "uuid",
  "risk_level": "medium"
}
```

---

## Get Protocol

GET /protocols/{id}

---

## Submit Protocol

POST /protocols/{id}/submit

---

## Withdraw Protocol

POST /protocols/{id}/withdraw

---

# 5. Reviews

## Assign Reviewer

POST /protocols/{id}/assign-reviewer

Request:
```json
{
  "reviewer_id": "uuid"
}
```

---

## Submit Review

POST /reviews

Request:
```json
{
  "protocol_id": "uuid",
  "score": 4,
  "recommendation": "minor revision",
  "comments": "..."
}
```

---

# 6. Committee Meetings

POST /meetings
GET /meetings/{id}

POST /meetings/{id}/agenda

POST /meetings/{id}/vote

---

# 7. Decisions

POST /decisions

GET /protocols/{id}/decision

---

# 8. Amendments

POST /protocols/{id}/amendments

GET /protocols/{id}/amendments

---

# 9. Documents

POST /protocols/{id}/documents
GET /documents/{id}

---

# 10. Audit

GET /audit-logs

---

# 11. Workflow Triggers

POST /workflow/advance

Description:
State transition trigger (internal use only)

---

# 12. Error Codes

- 400 Invalid input
- 401 Unauthorized
- 403 Forbidden
- 404 Not found
- 409 Conflict state