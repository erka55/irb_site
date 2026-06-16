# ERD Specification

Version: 1.0
Status: Freeze Candidate

---

# 1. Identity Domain

## TENANTS

| Column     | Type      | Notes  |
| ---------- | --------- | ------ |
| id         | UUID      | PK     |
| name       | VARCHAR   |        |
| code       | VARCHAR   | Unique |
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

| Column | Type    | Notes  |
| ------ | ------- | ------ |
| id     | UUID    | PK     |
| name   | VARCHAR |        |
| code   | VARCHAR | Unique |

---

## PERMISSIONS

| Column      | Type    | Notes  |
| ----------- | ------- | ------ |
| id          | UUID    | PK     |
| code        | VARCHAR | Unique |
| description | TEXT    |        |

---

## USER_ROLES

| Column  | Type | Notes      |
| ------- | ---- | ---------- |
| user_id | UUID | FK → USERS |
| role_id | UUID | FK → ROLES |

---

## ROLE_PERMISSIONS

| Column        | Type | Notes            |
| ------------- | ---- | ---------------- |
| role_id       | UUID | FK → ROLES       |
| permission_id | UUID | FK → PERMISSIONS |

---

Relationships

```text
TENANT 1 → N USERS

USER N ↔ N ROLES

ROLE N ↔ N PERMISSIONS
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

---

## COMMITTEE_MEMBERS

| Column       | Type    | Notes                    |
| ------------ | ------- | ------------------------ |
| id           | UUID    | PK                       |
| committee_id | UUID    | FK                       |
| user_id      | UUID    | FK                       |
| role         | VARCHAR | Chair, Member, Secretary |

---

Relationships

```text
COMMITTEE 1 → N COMMITTEE_MEMBERS

USER 1 → N COMMITTEE_MEMBERS
```

---

# 3. Protocol Domain

## PROTOCOLS

| Column                    | Type      | Notes                  |
| ------------------------- | --------- | ---------------------- |
| id                        | UUID      | PK                     |
| tenant_id                 | UUID      | FK                     |
| protocol_number           | VARCHAR   |                        |
| title                     | VARCHAR   |                        |
| principal_investigator_id | UUID      | FK → USERS             |
| workflow_state            | VARCHAR   |                        |
| current_version_id        | UUID      | FK → PROTOCOL_VERSIONS |
| submitted_at              | TIMESTAMP |                        |

---

## PROTOCOL_VERSIONS

| Column      | Type    | Notes |
| ----------- | ------- | ----- |
| id          | UUID    | PK    |
| protocol_id | UUID    | FK    |
| version_no  | INTEGER |       |
| summary     | TEXT    |       |

---

## DOCUMENTS

| Column              | Type    | Notes |
| ------------------- | ------- | ----- |
| id                  | UUID    | PK    |
| protocol_version_id | UUID    | FK    |
| document_type       | VARCHAR |       |
| file_path           | VARCHAR |       |
| file_size           | BIGINT  |       |

---

Relationships

```text
PROTOCOL 1 → N PROTOCOL_VERSIONS

PROTOCOL_VERSION 1 → N DOCUMENTS
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

---

## REVIEWS

| Column         | Type      | Notes |
| -------------- | --------- | ----- |
| id             | UUID      | PK    |
| assignment_id  | UUID      | FK    |
| recommendation | VARCHAR   |       |
| comments       | TEXT      |       |
| submitted_at   | TIMESTAMP |       |

---

Relationships

```text
PROTOCOL 1 → N REVIEW_ASSIGNMENTS

USER 1 → N REVIEW_ASSIGNMENTS

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
| status       | VARCHAR |       |

---

## AGENDA_ITEMS

| Column      | Type | Notes |
| ----------- | ---- | ----- |
| id          | UUID | PK    |
| meeting_id  | UUID | FK    |
| protocol_id | UUID | FK    |

---

## VOTES

| Column         | Type    | Notes |
| -------------- | ------- | ----- |
| id             | UUID    | PK    |
| agenda_item_id | UUID    | FK    |
| voter_id       | UUID    | FK    |
| vote           | VARCHAR |       |

---

Relationships

```text
MEETING 1 → N AGENDA_ITEMS

AGENDA_ITEM 1 → N VOTES
```

---

# 6. Decision Domain

## DECISIONS

| Column        | Type      | Notes |
| ------------- | --------- | ----- |
| id            | UUID      | PK    |
| protocol_id   | UUID      | FK    |
| decision_type | VARCHAR   |       |
| issued_at     | TIMESTAMP |       |

---

## AMENDMENTS

| Column         | Type      | Notes |
| -------------- | --------- | ----- |
| id             | UUID      | PK    |
| protocol_id    | UUID      | FK    |
| amendment_type | VARCHAR   |       |
| submitted_at   | TIMESTAMP |       |

---

Relationships

```text
PROTOCOL 1 → N DECISIONS

PROTOCOL 1 → N AMENDMENTS
```

---

# 7. Monitoring Domain

## PROGRESS_REPORTS

## ADVERSE_EVENTS

## APPEALS

All linked to:

```text
protocol_id → PROTOCOLS
```

Relationships

```text
PROTOCOL 1 → N PROGRESS_REPORTS

PROTOCOL 1 → N ADVERSE_EVENTS

PROTOCOL 1 → N APPEALS
```

---

# 8. Infrastructure Domain

## NOTIFICATIONS

| Column  | Type    | Notes |
| ------- | ------- | ----- |
| id      | UUID    | PK    |
| user_id | UUID    | FK    |
| title   | VARCHAR |       |
| message | TEXT    |       |
| is_read | BOOLEAN |       |

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

---

# ERD Design Rules

* UUID primary keys everywhere
* Tenant isolation mandatory
* Soft delete support
* Audit logging mandatory
* Workflow state stored in PROTOCOLS
* Decision records immutable after publication

---
