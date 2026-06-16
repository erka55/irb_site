# Django Model Mapping

Version: 1.0
Status: Freeze Candidate

---

# 1. Shared Abstract Models

## BaseModel

Abstract model used by all entities.

Fields:

```python
id = models.UUIDField(primary_key=True)

created_at = models.DateTimeField(auto_now_add=True)

updated_at = models.DateTimeField(auto_now=True)
```

---

## TenantModel

Extends BaseModel.

Fields:

```python
tenant = models.ForeignKey(
    Tenant,
    on_delete=models.PROTECT
)
```

Abstract:

```python
abstract = True
```

Used By:

* Committee
* Protocol
* Meeting
* Decision
* Amendment
* ProgressReport
* AdverseEvent
* Appeal

---

## AuditMixin

Fields:

```python
created_by

updated_by
```

Abstract:

```python
abstract = True
```

---

## SoftDeleteMixin

Fields:

```python
is_deleted

deleted_at

deleted_by
```

Abstract:

```python
abstract = True
```

---

# 2. Identity Models

## Tenant

Table:

```text
tenants
```

Fields:

```python
name

code

is_active
```

---

## User

Extends:

```python
AbstractUser
```

Table:

```text
users
```

Additional Fields:

```python
tenant

phone

job_title

is_active
```

Relationships:

```python
tenant -> Tenant
```

---

## Role

Table:

```text
roles
```

Fields:

```python
name

code

description
```

---

## Permission

Table:

```text
permissions
```

Fields:

```python
code

description
```

---

## UserRole

Table:

```text
user_roles
```

Relationships:

```python
user -> User

role -> Role
```

Unique Constraint:

```python
(user, role)
```

---

## RolePermission

Table:

```text
role_permissions
```

Relationships:

```python
role -> Role

permission -> Permission
```

Unique Constraint:

```python
(role, permission)
```

---

# 3. Committee Models

## Committee

Table:

```text
committees
```

Inherits:

```python
TenantModel
AuditMixin
```

Fields:

```python
name

description

is_active
```

---

## CommitteeMember

Table:

```text
committee_members
```

Relationships:

```python
committee

user
```

Fields:

```python
member_role
```

Examples:

```text
CHAIR

MEMBER

SECRETARY
```

---

# 4. Protocol Models

## Protocol

Table:

```text
protocols
```

Inherits:

```python
TenantModel

AuditMixin

SoftDeleteMixin
```

Relationships:

```python
principal_investigator

current_version
```

Fields:

```python
protocol_number

title

submission_type

review_type

workflow_state

submitted_at
```

---

## ProtocolVersion

Table:

```text
protocol_versions
```

Relationships:

```python
protocol
```

Fields:

```python
version_no

summary

change_notes
```

---

## Document

Table:

```text
documents
```

Relationships:

```python
protocol_version
```

Fields:

```python
document_type

file_name

file_path

file_size

mime_type
```

---

# 5. Review Models

## ReviewAssignment

Table:

```text
review_assignments
```

Relationships:

```python
protocol

reviewer
```

Fields:

```python
assigned_at

due_date

status
```

---

## Review

Table:

```text
reviews
```

Relationships:

```python
assignment
```

Fields:

```python
recommendation

comments

submitted_at
```

Examples:

```text
APPROVE

MODIFICATION_REQUIRED

DEFER

REJECT
```

---

# 6. Meeting Models

## Meeting

Table:

```text
meetings
```

Relationships:

```python
committee
```

Fields:

```python
meeting_date

location

status
```

---

## AgendaItem

Table:

```text
agenda_items
```

Relationships:

```python
meeting

protocol
```

Fields:

```python
sequence_no
```

---

## Vote

Table:

```text
votes
```

Relationships:

```python
agenda_item

voter
```

Fields:

```python
vote

comments
```

Examples:

```text
APPROVE

DISAPPROVE

ABSTAIN
```

---

# 7. Decision Models

## Decision

Table:

```text
decisions
```

Relationships:

```python
protocol
```

Fields:

```python
decision_type

decision_text

issued_at

published_at
```

Examples:

```text
APPROVED

APPROVED_WITH_CONDITIONS

DEFERRED

REJECTED
```

Notes:

```text
Immutable after publication.
```

---

## Amendment

Table:

```text
amendments
```

Relationships:

```python
protocol
```

Fields:

```python
amendment_type

description

submitted_at
```

---

# 8. Monitoring Models

## ProgressReport

Table:

```text
progress_reports
```

Relationships:

```python
protocol
```

Fields:

```python
report_period

summary

submitted_at
```

---

## AdverseEvent

Table:

```text
adverse_events
```

Relationships:

```python
protocol
```

Fields:

```python
event_date

severity

description
```

---

## Appeal

Table:

```text
appeals
```

Relationships:

```python
protocol
```

Fields:

```python
reason

submitted_at

status
```

---

# 9. Infrastructure Models

## Notification

Table:

```text
notifications
```

Relationships:

```python
user
```

Fields:

```python
title

message

is_read

read_at
```

---

## AuditEvent

Table:

```text
audit_events
```

Relationships:

```python
actor
```

Fields:

```python
entity_type

entity_id

action

payload

created_at
```

Design:

```text
Generic entity reference

No FK to business entities
```

Examples:

```text
protocol_submitted

review_assigned

decision_published
```

---

# 10. Future Reserved Models

Reserved For:

```python
WorkflowDefinition

WorkflowTransition

RuleDefinition

AIProtocolAssessment

AIReviewSuggestion

ExternalRegistryLink
```

---

# Model Design Rules

## Primary Keys

```text
UUID everywhere
```

---

## Multi-Tenancy

```text
Tenant isolation required
```

---

## Soft Delete

Used for:

```text
Protocols

Documents

Users (optional)
```

---

## Audit

All business entities must support:

```text
created_by

updated_by
```

---

## Workflow

Workflow state is stored in:

```text
Protocol.workflow_state
```

Workflow engine controls transitions.

---

## Decision Immutability

Published decisions:

```text
Cannot be modified

Cannot be deleted
```

Must create a new decision record instead.

---

# Freeze Candidate Notes

This document maps:

* ERD v1.0
* database-schema.md
* workflow.md
* rbac.md

to Django ORM implementation and serves as the authoritative source for model creation.

---
