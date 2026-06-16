# Django Model Mapping

Version: 1.1
Status: Final

---

# Purpose

This document maps:

* erd-v1.1.md
* database-schema-v1.1.md

to Django ORM models.

This specification is the authoritative source for:

* Django applications
* Django models
* Initial migrations
* Service layer implementation

---

# Django Project Structure

```text
apps/

├── accounts
├── committees
├── protocols
├── reviews
├── meetings
├── decisions
├── monitoring
├── notifications
└── audit
```

---

# Shared Base Models

## BaseModel

Abstract model.

```python
class BaseModel(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
```

---

## TenantModel

```python
class TenantModel(BaseModel):

    tenant = models.ForeignKey(
        "accounts.Tenant",
        on_delete=models.PROTECT
    )

    class Meta:
        abstract = True
```

---

## AuditMixin

```python
class AuditMixin(models.Model):

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="+",
        on_delete=models.PROTECT
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="+",
        on_delete=models.PROTECT
    )

    class Meta:
        abstract = True
```

---

## SoftDeleteMixin

```python
class SoftDeleteMixin(models.Model):

    is_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
```

---

# accounts App

## Tenant

```python
class Tenant(BaseModel):
    name
    code
    is_active
```

Meta

```python
db_table = "tenants"
```

---

## User

```python
class User(AbstractUser):

    tenant

    phone

    job_title
```

Meta

```python
db_table = "users"
```

Constraint

```python
UniqueConstraint(
    fields=["tenant", "email"]
)
```

---

## Role

```python
class Role(BaseModel):
    name
    code
    description
```

---

## Permission

```python
class Permission(BaseModel):
    code
    description
```

---

## UserRole

```python
class UserRole(BaseModel):

    user

    role
```

Constraint

```python
UniqueConstraint(
    fields=["user", "role"]
)
```

---

## RolePermission

```python
class RolePermission(BaseModel):

    role

    permission
```

Constraint

```python
UniqueConstraint(
    fields=["role", "permission"]
)
```

---

# committees App

## Committee

Inheritance

```python
TenantModel
AuditMixin
```

Fields

```python
name

description

is_active
```

---

## CommitteeMember

Fields

```python
committee

user

member_role
```

Choices

```python
CHAIR

MEMBER

SECRETARY
```

Constraint

```python
UniqueConstraint(
    fields=["committee", "user"]
)
```

---

# protocols App

## Protocol

Inheritance

```python
TenantModel
AuditMixin
SoftDeleteMixin
```

Fields

```python
protocol_number

title

workflow_state

submitted_at
```

Relationships

```python
principal_investigator

current_version
```

Indexes

```python
tenant

workflow_state

protocol_number

submitted_at
```

---

## ProtocolVersion

Fields

```python
protocol

version_no

summary

change_notes
```

Constraint

```python
UniqueConstraint(
    fields=["protocol", "version_no"]
)
```

---

## Document

Inheritance

```python
SoftDeleteMixin
```

Fields

```python
protocol_version

document_type

file_name

file_path

file_size

mime_type
```

---

## ProtocolComment

Fields

```python
protocol

author

comment_type

comment_text

is_internal
```

Choices

```python
SCREENING

REVIEW

CHAIR

INTERNAL
```

---

## WorkflowHistory

Fields

```python
protocol

from_state

to_state

event

performed_by

performed_at
```

Indexes

```python
protocol

performed_at
```

---

# reviews App

## ReviewAssignment

Fields

```python
protocol

reviewer

assigned_at

due_date

status
```

Constraint

```python
UniqueConstraint(
    fields=["protocol", "reviewer"]
)
```

---

## Review

Fields

```python
assignment

recommendation

comments

submitted_at
```

Relationship

```python
OneToOneField(
    ReviewAssignment
)
```

Choices

```python
APPROVE

MODIFICATION_REQUIRED

DEFER

REJECT
```

---

# meetings App

## Meeting

Inheritance

```python
TenantModel
AuditMixin
```

Fields

```python
committee

meeting_date

location

status
```

---

## AgendaItem

Fields

```python
meeting

protocol

sequence_no
```

---

## Vote

Fields

```python
agenda_item

voter

vote

comments
```

Constraint

```python
UniqueConstraint(
    fields=["agenda_item", "voter"]
)
```

Choices

```python
APPROVE

DISAPPROVE

ABSTAIN
```

---

# decisions App

## Decision

Inheritance

```python
AuditMixin
```

Fields

```python
protocol

decision_type

decision_text

metadata

issued_at

published_at
```

Field Type

```python
metadata = models.JSONField(
    null=True,
    blank=True
)
```

Choices

```python
INITIAL_APPROVAL

CONTINUING_REVIEW

AMENDMENT_APPROVAL

SUSPENSION

TERMINATION

CLOSURE
```

Business Rule

```text
Published decisions are immutable.
```

---

## Amendment

Fields

```python
protocol

amendment_type

description

submitted_at
```

---

# monitoring App

## ProgressReport

Fields

```python
protocol

report_period

summary

submitted_at
```

---

## AdverseEvent

Fields

```python
protocol

event_date

severity

description
```

---

## Appeal

Fields

```python
protocol

reason

submitted_at

status
```

---

# notifications App

## Notification

Fields

```python
user

title

message

is_read

read_at
```

Indexes

```python
user

is_read
```

---

# audit App

## AuditEvent

Fields

```python
actor

entity_type

entity_id

action

payload
```

Field Type

```python
payload = models.JSONField(
    null=True,
    blank=True
)
```

Indexes

```python
entity_type

entity_id

actor

created_at
```

Business Rules

```text
Immutable

Never deleted
```

---

# Application Ownership Matrix

| App           | Models                                                                |
| ------------- | --------------------------------------------------------------------- |
| accounts      | Tenant, User, Role, Permission, UserRole, RolePermission              |
| committees    | Committee, CommitteeMember                                            |
| protocols     | Protocol, ProtocolVersion, Document, ProtocolComment, WorkflowHistory |
| reviews       | ReviewAssignment, Review                                              |
| meetings      | Meeting, AgendaItem, Vote                                             |
| decisions     | Decision, Amendment                                                   |
| monitoring    | ProgressReport, AdverseEvent, Appeal                                  |
| notifications | Notification                                                          |
| audit         | AuditEvent                                                            |

---

# Final Freeze Notes

This mapping is aligned with:

* architecture-v0.2.md
* workflow-v1.0.md
* rbac-v1.0.md
* api-spec-v1.0.md
* erd-v1.1.md
* database-schema-v1.1.md

No model structure changes should be introduced after this version without a migration plan.

---
