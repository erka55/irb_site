# IRB System API Specification

Version: 1.0
Status: Freeze Candidate

---

# 1. API Overview

Base URL:

```text
/api/v1
```

Architecture Style:

- REST API
- JSON Request/Response
- JWT Authentication
- Multi-Tenant Aware

---

# 2. Authentication

Authentication Method:

```text
Bearer JWT Token
```

Header:

```http
Authorization: Bearer <token>
```

---

# 3. Standard Response Format

## Success

```json
{
  "success": true,
  "data": {},
  "message": null
}
```

## Error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request"
  }
}
```

---

# 4. Authentication API

## Login

```http
POST /auth/login
```

Request:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Response:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "user": {}
}
```

---

## Refresh Token

```http
POST /auth/refresh
```

---

## Logout

```http
POST /auth/logout
```

---

## Current User

```http
GET /auth/me
```

---

# 5. User Management API

## List Users

```http
GET /users
```

Permission:

```text
user.view
```

---

## Create User

```http
POST /users
```

Permission:

```text
user.create
```

---

## Get User

```http
GET /users/{id}
```

---

## Update User

```http
PATCH /users/{id}
```

---

## Disable User

```http
POST /users/{id}/disable
```

---

# 6. Committee API

## List Committees

```http
GET /committees
```

---

## Create Committee

```http
POST /committees
```

---

## Committee Details

```http
GET /committees/{id}
```

---

## Update Committee

```http
PATCH /committees/{id}
```

---

## Add Committee Member

```http
POST /committees/{id}/members
```

---

## Remove Committee Member

```http
DELETE /committees/{id}/members/{memberId}
```

---

# 7. Protocol API

## List Protocols

```http
GET /protocols
```

Filters:

```text
workflow_state
submission_type
review_type
principal_investigator
```

---

## Create Protocol

```http
POST /protocols
```

Permission:

```text
protocol.create
```

---

## Protocol Detail

```http
GET /protocols/{id}
```

---

## Update Protocol

```http
PATCH /protocols/{id}
```

Permission:

```text
protocol.edit
```

---

## Submit Protocol

```http
POST /protocols/{id}/submit
```

Workflow Event:

```text
submit_protocol
```

---

## Withdraw Protocol

```http
POST /protocols/{id}/withdraw
```

Workflow Event:

```text
withdraw_protocol
```

---

# 8. Protocol Version API

## Create New Version

```http
POST /protocols/{id}/versions
```

---

## List Versions

```http
GET /protocols/{id}/versions
```

---

## Get Version

```http
GET /protocols/{id}/versions/{versionId}
```

---

# 9. Document API

## Upload Document

```http
POST /documents
```

Content-Type:

```text
multipart/form-data
```

---

## Download Document

```http
GET /documents/{id}/download
```

---

## Delete Document

```http
DELETE /documents/{id}
```

---

# 10. Review Assignment API

## Assign Reviewer

```http
POST /review-assignments
```

Permission:

```text
review_assignment.create
```

---

## List Assignments

```http
GET /review-assignments
```

---

# 11. Review API

## Create Review

```http
POST /reviews
```

Permission:

```text
review.create
```

---

## Update Review

```http
PATCH /reviews/{id}
```

---

## Submit Review

```http
POST /reviews/{id}/submit
```

Workflow Validation:

```text
state == REVIEW
```

---

## List Reviews

```http
GET /reviews
```

---

# 12. Meeting API

## Create Meeting

```http
POST /meetings
```

---

## List Meetings

```http
GET /meetings
```

---

## Meeting Detail

```http
GET /meetings/{id}
```

---

## Update Meeting

```http
PATCH /meetings/{id}
```

---

## Close Meeting

```http
POST /meetings/{id}/close
```

Workflow Event:

```text
meeting_completed
```

---

# 13. Agenda API

## Add Agenda Item

```http
POST /meetings/{id}/agenda
```

---

## Remove Agenda Item

```http
DELETE /agenda/{id}
```

---

# 14. Voting API

## Submit Vote

```http
POST /votes
```

Request:

```json
{
  "agenda_item_id": "uuid",
  "vote": "APPROVE"
}
```

---

## List Votes

```http
GET /agenda/{id}/votes
```

---

# 15. Decision API

## Create Decision

```http
POST /decisions
```

Permission:

```text
decision.create
```

---

## Publish Decision

```http
POST /decisions/{id}/publish
```

Permission:

```text
decision.publish
```

---

## Decision Detail

```http
GET /decisions/{id}
```

---

# 16. Amendment API

## Create Amendment

```http
POST /amendments
```

---

## Submit Amendment

```http
POST /amendments/{id}/submit
```

---

## Approve Amendment

```http
POST /amendments/{id}/approve
```

---

# 17. Progress Report API

## Create Report

```http
POST /progress-reports
```

---

## Submit Report

```http
POST /progress-reports/{id}/submit
```

---

## List Reports

```http
GET /progress-reports
```

---

# 18. Adverse Event API

## Report Event

```http
POST /adverse-events
```

---

## List Events

```http
GET /adverse-events
```

---

# 19. Appeal API

## Submit Appeal

```http
POST /appeals
```

---

## Review Appeal

```http
POST /appeals/{id}/review
```

---

## Decide Appeal

```http
POST /appeals/{id}/decide
```

---

# 20. Notification API

## My Notifications

```http
GET /notifications
```

---

## Mark Read

```http
POST /notifications/{id}/read
```

---

# 21. Audit API

## Audit Log Search

```http
GET /audit-events
```

Filters:

```text
entity_type
entity_id
actor_id
date_from
date_to
```

Permission:

```text
audit.view
```

---

# 22. Workflow API

## Available Actions

```http
GET /protocols/{id}/available-actions
```

Example Response:

```json
{
  "actions": [
    "submit_protocol",
    "edit_protocol"
  ]
}
```

---

## Execute Workflow Event

```http
POST /protocols/{id}/workflow
```

Request:

```json
{
  "event": "submit_protocol"
}
```

---

# 23. RBAC Enforcement

Every endpoint must validate:

```text
Authentication
+
Tenant Isolation
+
Permission Check
+
Workflow Rules
+
Ownership Rules
+
Conflict of Interest Rules
```

---

# 24. API Versioning

Current Version:

```text
v1
```

Base URL:

```text
/ api/v1
```

Future Versions:

```text
/ api/v2
```

---

# 25. OpenAPI Compatibility

This specification is intended to be implemented as:

- Django REST Framework
- OpenAPI 3.1
- Swagger UI
- ReDoc

---