# Database Schema Specification

Version: 1.0
Status: Freeze Candidate

---

# 1. General Design Rules

## Primary Keys

All tables use UUID as primary key.

```sql
id UUID PRIMARY KEY
```

---

## Tenant Isolation

All business entities must contain:

```sql
tenant_id UUID NOT NULL
```

except:

- permissions
- roles
- role_permissions

which are global reference tables.

---

## Audit Columns

All business entities include:

```sql
created_at TIMESTAMP NOT NULL
created_by UUID

updated_at TIMESTAMP
updated_by UUID
```

---

## Soft Delete

All business entities support:

```sql
is_deleted BOOLEAN DEFAULT FALSE

deleted_at TIMESTAMP NULL
deleted_by UUID NULL
```

Physical deletion is prohibited except for system maintenance.

---

# 2. Identity Domain

## tenants

```sql
id UUID PK

name VARCHAR(255)
code VARCHAR(50)

status VARCHAR(50)

created_at TIMESTAMP
```

### Constraints

```sql
UNIQUE(code)
```

---

## users

```sql
id UUID PK

tenant_id UUID FK

email VARCHAR(255)

password_hash TEXT

first_name VARCHAR(255)
last_name VARCHAR(255)

title VARCHAR(255)

status VARCHAR(50)

created_at TIMESTAMP
updated_at TIMESTAMP
```

### Constraints

```sql
UNIQUE(tenant_id, email)
```

### Foreign Keys

```sql
tenant_id
    REFERENCES tenants(id)
```

---

## roles

```sql
id UUID PK

code VARCHAR(100)
name VARCHAR(255)

description TEXT
```

### Constraints

```sql
UNIQUE(code)
```

---

## permissions

```sql
id UUID PK

code VARCHAR(255)
name VARCHAR(255)
```

### Constraints

```sql
UNIQUE(code)
```

---

## role_permissions

```sql
role_id UUID FK
permission_id UUID FK
```

### Constraints

```sql
PRIMARY KEY(role_id, permission_id)
```

---

## user_roles

```sql
user_id UUID FK
role_id UUID FK
```

### Constraints

```sql
PRIMARY KEY(user_id, role_id)
```

---

# 3. Committee Domain

## committees

```sql
id UUID PK

tenant_id UUID FK

name VARCHAR(255)

description TEXT

active BOOLEAN
```

### Constraints

```sql
UNIQUE(tenant_id, name)
```

---

## committee_members

```sql
id UUID PK

committee_id UUID FK
user_id UUID FK

role_in_committee VARCHAR(100)

start_date DATE
end_date DATE
```

### Constraints

```sql
UNIQUE(committee_id, user_id)
```

---

# 4. Protocol Domain

## protocols

```sql
id UUID PK

tenant_id UUID FK

protocol_number VARCHAR(100)

title TEXT

principal_investigator_id UUID FK

workflow_state VARCHAR(100)

submission_type VARCHAR(100)
review_type VARCHAR(100)

current_version_id UUID NULL
```

### Constraints

```sql
UNIQUE(tenant_id, protocol_number)
```

### Indexes

```sql
INDEX(workflow_state)

INDEX(principal_investigator_id)
```

---

## protocol_versions

```sql
id UUID PK

protocol_id UUID FK

version_number INTEGER

status VARCHAR(100)

submitted_at TIMESTAMP
```

### Constraints

```sql
UNIQUE(protocol_id, version_number)
```

---

## documents

```sql
id UUID PK

protocol_version_id UUID FK

document_type VARCHAR(100)

file_name TEXT

storage_path TEXT

uploaded_by UUID

uploaded_at TIMESTAMP
```

---

# 5. Review Domain

## review_assignments

```sql
id UUID PK

protocol_id UUID FK

reviewer_id UUID FK

assigned_date TIMESTAMP

due_date TIMESTAMP

status VARCHAR(50)
```

### Constraints

```sql
UNIQUE(protocol_id, reviewer_id)
```

---

## reviews

```sql
id UUID PK

assignment_id UUID FK

recommendation VARCHAR(100)

comments TEXT

submitted_at TIMESTAMP
```

### Constraints

```sql
UNIQUE(assignment_id)
```

---

# 6. Meeting Domain

## meetings

```sql
id UUID PK

committee_id UUID FK

meeting_date TIMESTAMP

quorum_required INTEGER

status VARCHAR(50)
```

### Indexes

```sql
INDEX(meeting_date)
```

---

## agenda_items

```sql
id UUID PK

meeting_id UUID FK

protocol_id UUID FK

order_number INTEGER
```

### Constraints

```sql
UNIQUE(meeting_id, protocol_id)

UNIQUE(meeting_id, order_number)
```

---

## votes

```sql
id UUID PK

agenda_item_id UUID FK

voter_id UUID FK

vote VARCHAR(50)

cast_at TIMESTAMP
```

### Constraints

```sql
UNIQUE(agenda_item_id, voter_id)
```

---

# 7. Decision Domain

## decisions

```sql
id UUID PK

protocol_id UUID FK

decision_type VARCHAR(100)

decision_date DATE

effective_date DATE

decision_letter_path TEXT
```

### Indexes

```sql
INDEX(protocol_id)
```

---

## amendments

```sql
id UUID PK

protocol_id UUID FK

amendment_type VARCHAR(100)

description TEXT

status VARCHAR(100)
```

---

# 8. Monitoring Domain

## progress_reports

```sql
id UUID PK

protocol_id UUID FK

report_period VARCHAR(100)

summary TEXT

submitted_at TIMESTAMP
```

---

## adverse_events

```sql
id UUID PK

protocol_id UUID FK

severity VARCHAR(50)

description TEXT

reported_at TIMESTAMP
```

---

## appeals

```sql
id UUID PK

protocol_id UUID FK

appellant_id UUID FK

appeal_reason TEXT

status VARCHAR(50)

submitted_at TIMESTAMP
```

---

# 9. Workflow Domain

## workflow_definitions

```sql
id UUID PK

name VARCHAR(255)

version INTEGER

active BOOLEAN
```

### Constraints

```sql
UNIQUE(name, version)
```

---

## workflow_transitions

```sql
id UUID PK

workflow_id UUID FK

from_state VARCHAR(100)

to_state VARCHAR(100)

event_name VARCHAR(100)
```

### Constraints

```sql
UNIQUE(workflow_id, from_state, event_name)
```

---

# 10. Notification Domain

## notifications

```sql
id UUID PK

user_id UUID FK

channel VARCHAR(50)

subject TEXT

message TEXT

sent_at TIMESTAMP
```

### Indexes

```sql
INDEX(user_id)
```

---

# 11. Audit Domain

## audit_events

```sql
id UUID PK

tenant_id UUID FK

actor_id UUID FK

entity_type VARCHAR(100)

entity_id UUID

action VARCHAR(100)

payload JSONB

created_at TIMESTAMP
```

### Indexes

```sql
INDEX(created_at)

INDEX(entity_type, entity_id)

GIN(payload)
```

---

# 12. Foreign Key Delete Rules

## RESTRICT

Never allow deletion if referenced:

```text
tenants
users
protocols
decisions
reviews
audit_events
```

---

## CASCADE

Allowed only for:

```text
protocol_versions
documents

role_permissions
user_roles
committee_members
```

---

## SET NULL

Allowed for:

```text
updated_by
deleted_by
```

when user account becomes inactive.

---

# 13. PostgreSQL Row-Level Security

All tenant-owned tables must enforce:

```sql
tenant_id = current_tenant()
```

Protected Tables:

- users
- committees
- protocols
- protocol_versions
- reviews
- meetings
- decisions
- notifications
- audit_events

---

# 14. Performance Indexes

Mandatory indexes:

```sql
users(email)

protocols(protocol_number)

protocols(workflow_state)

review_assignments(reviewer_id)

meetings(meeting_date)

notifications(user_id)

audit_events(created_at)

audit_events(entity_type, entity_id)
```

---

# 15. Freeze Status

This schema is considered:

Production-Ready v1.0

Approved Inputs:

- architecture.md v0.2
- data-model.md v0.1
- rbac.md v1.0

This document serves as the basis for:

- Django Models
- Database Migrations
- API Design
- Workflow Implementation

---