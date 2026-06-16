# ERD Specification

Version: 1.1
Status: Final Freeze

---

# Purpose

This document defines the final Entity Relationship Design (ERD) for the IRB System MVP.

This ERD serves as the authoritative source for:

* database-schema.md
* django-model-mapping.md
* Django migrations
* API implementation

---

# 1. Identity Domain

## TENANTS

| Column     | Type      | Notes  |
| ---------- | --------- | ------ |
| id         | UUID      | PK     |
| name       | VARCHAR   |        |
| code       | VARCHAR   | UNIQUE |
| is_active  | BOOLEAN   |        |
| created_at | TIMESTAMP |        |
| updated_at | TIMESTAMP |        |

---

## USERS

| Column     | Type      | Notes             |
| ---------- | --------- | ----------------- |
| id         | UUID      | PK                |
| tenant_id  | UUID      | FK → TENANTS      |
| email      | VARCHAR   | Unique per tenant |
| first_name | VARCHAR   |                   |
| last_name  | VARCHAR   |                   |
| is_active  | BOOLEAN   |                   |
| created_at | TIMESTAMP |                   |
| updated_at | TIMESTAMP |                   |

---

## ROLES

| Column      | Type    | Notes  |
| ----------- | ------- | ------ |
| id          | UUID    | PK     |
| name        | VARCHAR |        |
| code        | VARCHAR | UNIQUE |
| description | TEXT    |        |

---

## PERMISSIONS

| Column      | Type    | Notes  |
| ----------- | ------- | ------ |
| id          | UUID    | PK     |
| code        | VARCHAR | UNIQUE |
| description | TEXT    |        |

---

## USER_ROLES

| Column  | Type | Notes      |
| ------- | ---- | ---------- |
| user_id | UUID | FK → USERS |
| role_id | UUID | FK → ROLES |

Constraint:

```text
UNIQUE(user_id, role_id)
```

---

## ROLE_PERMISSIONS

| Column        | Type | Notes            |
| ------------- | ---- | ---------------- |
| role_id       | UUID | FK → ROLES       |
| permission_id | UUID | FK → PERMISSIONS |

Constraint:

```text
UNIQUE(role_id, permission_id)
```

---

# 2. Committee Domain

## COMMITTEES

| Column      | Type    | Notes |
| ----------- | ------- | ----- |
| id          | UUID    | PK    |
| tenant_id   | UUID    | FK    |
| name        | VARCHAR |       |
| description | TEXT    |       |
| is_active   | BOOLEAN |       |

---

## COMMITTEE_MEMBERS

| Column       | Type    | Notes |
| ------------ | ------- | ----- |
| id           | UUID    | PK    |
| committee_id | UUID    | FK    |
| user_id      | UUID    | FK    |
| member_role  | VARCHAR |       |

Constraint:

```text
UNIQUE(committee_id, user_id)
```

---

# 3. Protocol Domain

## PROTOCOLS

| Column                    | Type      | Notes                  |
| ------------------------- | --------- | ---------------------- |
| id                        | UUID      | PK                     |
| tenant_id                 | UUID      | FK                     |
| protocol_number           | VARCHAR   | Indexed                |
| title                     | VARCHAR   |                        |
| principal_investigator_id | UUID      | FK → USERS             |
| workflow_state            | VARCHAR   | Indexed                |
| current_version_id        | UUID      | FK → PROTOCOL_VERSIONS |
| submitted_at              | TIMESTAMP | Indexed                |
| is_deleted                | BOOLEAN   | Soft delete            |

Indexes:

```text
INDEX(tenant_id)
INDEX(protocol_number)
INDEX(workflow_state)
INDEX(submitted_at)
```

---

## PROTOCOL_VERSIONS

| Column       | Type    | Notes |
| ------------ | ------- | ----- |
| id           | UUID    | PK    |
| protocol_id  | UUID    | FK    |
| version_no   | INTEGER |       |
| summary      | TEXT    |       |
| change_notes | TEXT    |       |

Constraint:

```text
UNIQUE(protocol_id, version_no)
```

---

## DOCUMENTS

| Column              | Type    | Notes |
| ------------------- | ------- | ----- |
| id                  | UUID    | PK    |
| protocol_version_id | UUID    | FK    |
| document_type       | VARCHAR |       |
| file_name           | VARCHAR |       |
| file_path           | VARCHAR |       |
| file_size           | BIGINT  |       |
| mime_type           | VARCHAR |       |

---

## PROTOCOL_COMMENTS

| Column       | Type      | Notes      |
| ------------ | --------- | ---------- |
| id           | UUID      | PK         |
| protocol_id  | UUID      | FK         |
| author_id    | UUID      | FK → USERS |
| comment_type | VARCHAR   |            |
| comment_text | TEXT      |            |
| is_internal  | BOOLEAN   |            |
| created_at   | TIMESTAMP |            |

Examples:

```text
SCREENING
REVIEW
CHAIR
INTERNAL
```

---

## WORKFLOW_HISTORIES

| Column       | Type      | Notes      |
| ------------ | --------- | ---------- |
| id           | UUID      | PK         |
| protocol_id  | UUID      | FK         |
| from_state   | VARCHAR   |            |
| to_state     | VARCHAR   |            |
| event        | VARCHAR   |            |
| performed_by | UUID      | FK → USERS |
| performed_at | TIMESTAMP |            |

Indexes:

```text
INDEX(protocol_id)
INDEX(performed_at)
```

---

# 4. Review Domain

## REVIEW_ASSIGNMENTS

| Column      | Type      | Notes |
| ----------- | --------- | ----- |
| id          | UUID      | PK    |
| protocol_id | UUID      | FK    |
| reviewer_id | UUID      | FK    |
| assigned_at | TIMESTAMP |       |
| due_date    | DATE      |       |
| status      | VARCHAR   |       |

Constraint:

```text
UNIQUE(protocol_id, reviewer_id)
```

---

## REVIEWS

| Column         | Type      | Notes   |
| -------------- | --------- | ------- |
| id             | UUID      | PK      |
| assignment_id  | UUID      | FK      |
| recommendation | VARCHAR   |         |
| comments       | TEXT      |         |
| submitted_at   | TIMESTAMP | Indexed |

Relationship:

```text
REVIEW_ASSIGNMENT 1 → 1 REVIEW
```

---

# 5. Meeting Domain

## MEETINGS

| Column       | Type    | Notes |
| ------------ | ------- | ----- |
| id           | UUID    | PK    |
| committee_id | UUID    | FK    |
| meeting_date | DATE    |       |
| location     | VARCHAR |       |
| status       | VARCHAR |       |

---

## AGENDA_ITEMS

| Column      | Type    | Notes |
| ----------- | ------- | ----- |
| id          | UUID    | PK    |
| meeting_id  | UUID    | FK    |
| protocol_id | UUID    | FK    |
| sequence_no | INTEGER |       |

---

## VOTES

| Column         | Type    | Notes |
| -------------- | ------- | ----- |
| id             | UUID    | PK    |
| agenda_item_id | UUID    | FK    |
| voter_id       | UUID    | FK    |
| vote           | VARCHAR |       |
| comments       | TEXT    |       |

Constraint:

```text
UNIQUE(agenda_item_id, voter_id)
```

Values:

```text
APPROVE
DISAPPROVE
ABSTAIN
```

---

# 6. Decision Domain

## DECISIONS

| Column        | Type      | Notes   |
| ------------- | --------- | ------- |
| id            | UUID      | PK      |
| protocol_id   | UUID      | FK      |
| decision_type | VARCHAR   |         |
| decision_text | TEXT      |         |
| issued_at     | TIMESTAMP | Indexed |
| published_at  | TIMESTAMP |         |

Decision Types:

```text
INITIAL_APPROVAL
CONTINUING_REVIEW
AMENDMENT_APPROVAL
SUSPENSION
TERMINATION
CLOSURE
```

Rule:

```text
Immutable after publication
```

---

## AMENDMENTS

| Column         | Type      | Notes |
| -------------- | --------- | ----- |
| id             | UUID      | PK    |
| protocol_id    | UUID      | FK    |
| amendment_type | VARCHAR   |       |
| description    | TEXT      |       |
| submitted_at   | TIMESTAMP |       |

---

# 7. Monitoring Domain

## PROGRESS_REPORTS

| Column        | Type      | Notes |
| ------------- | --------- | ----- |
| id            | UUID      | PK    |
| protocol_id   | UUID      | FK    |
| report_period | VARCHAR   |       |
| summary       | TEXT      |       |
| submitted_at  | TIMESTAMP |       |

---

## ADVERSE_EVENTS

| Column      | Type    | Notes |
| ----------- | ------- | ----- |
| id          | UUID    | PK    |
| protocol_id | UUID    | FK    |
| event_date  | DATE    |       |
| severity    | VARCHAR |       |
| description | TEXT    |       |

---

## APPEALS

| Column       | Type      | Notes |
| ------------ | --------- | ----- |
| id           | UUID      | PK    |
| protocol_id  | UUID      | FK    |
| reason       | TEXT      |       |
| submitted_at | TIMESTAMP |       |
| status       | VARCHAR   |       |

---

# 8. Infrastructure Domain

## NOTIFICATIONS

| Column  | Type      | Notes |
| ------- | --------- | ----- |
| id      | UUID      | PK    |
| user_id | UUID      | FK    |
| title   | VARCHAR   |       |
| message | TEXT      |       |
| is_read | BOOLEAN   |       |
| read_at | TIMESTAMP |       |

---

## AUDIT_EVENTS

| Column      | Type      | Notes      |
| ----------- | --------- | ---------- |
| id          | UUID      | PK         |
| actor_id    | UUID      | FK → USERS |
| entity_type | VARCHAR   |            |
| entity_id   | UUID      |            |
| action      | VARCHAR   |            |
| payload     | JSONB     |            |
| created_at  | TIMESTAMP |            |

Indexes:

```text
INDEX(entity_type, entity_id)
INDEX(actor_id)
INDEX(created_at)
```

Rule:

```text
Never physically deleted
```

---

# Delete Rules

| Entity          | Rule        |
| --------------- | ----------- |
| Tenant          | PROTECT     |
| User            | PROTECT     |
| Committee       | PROTECT     |
| Protocol        | SOFT DELETE |
| Decision        | NO DELETE   |
| WorkflowHistory | NO DELETE   |
| AuditEvent      | NO DELETE   |

---

# Cardinality Summary

```text
TENANT 1 → N USERS

USER N ↔ N ROLES

ROLE N ↔ N PERMISSIONS

COMMITTEE 1 → N COMMITTEE_MEMBERS

PROTOCOL 1 → N PROTOCOL_VERSIONS

PROTOCOL_VERSION 1 → N DOCUMENTS

PROTOCOL 1 → N PROTOCOL_COMMENTS

PROTOCOL 1 → N WORKFLOW_HISTORIES

PROTOCOL 1 → N REVIEW_ASSIGNMENTS

REVIEW_ASSIGNMENT 1 → 1 REVIEW

MEETING 1 → N AGENDA_ITEMS

AGENDA_ITEM 1 → N VOTES

PROTOCOL 1 → N DECISIONS

PROTOCOL 1 → N AMENDMENTS

PROTOCOL 1 → N PROGRESS_REPORTS

PROTOCOL 1 → N ADVERSE_EVENTS

PROTOCOL 1 → N APPEALS
```

---

# Final Freeze Notes

This ERD is the authoritative model for:

* database-schema-v1.1.md
* django-model-mapping-v1.1.md
* Django migrations
* Backend implementation

No structural changes should be introduced after this version without an approved schema migration plan.

---
