# Backend MVP Specification

Version: 1.0
Status: Freeze

---

# 1. Purpose

This document defines the backend implementation architecture for the IRB System MVP.

The backend must support:

- Multi-tenancy
- Workflow-driven processing
- RBAC authorization
- Audit logging
- Document management
- Committee review lifecycle

This specification is based on:

- architecture.md
- data-model.md
- workflow.md
- rbac.md
- database-schema.md
- api-spec.md

---

# 2. Technology Stack

## Core Framework

```text
Python 3.13
Django 5.x
Django REST Framework
```

---

## Database

```text
PostgreSQL 18
```

---

## Cache

```text
Redis
```

---

## Background Jobs

```text
Celery
```

---

## API Documentation

```text
drf-spectacular
Swagger UI
ReDoc
```

---

## Testing

```text
pytest
pytest-django
factory-boy
```

---

## Deployment

```text
Docker
Docker Compose
```

---

# 3. Project Structure

```text
backend/
│
├── config/
│   ├── settings/
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│
│   ├── identity/
│   ├── committees/
│   ├── protocols/
│   ├── reviews/
│   ├── meetings/
│   ├── decisions/
│   ├── monitoring/
│   ├── workflow/
│   ├── notifications/
│   └── audit/
│
├── core/
│   ├── auth/
│   ├── permissions/
│   ├── tenancy/
│   ├── storage/
│   ├── events/
│   ├── exceptions/
│   └── utils/
│
├── tests/
│
└── manage.py
```

---

# 4. Domain Applications

## identity

Responsibilities:

- Authentication
- Users
- Roles
- Permissions
- Tenants

Tables:

```text
users
roles
permissions
user_roles
tenants
```

---

## committees

Responsibilities:

- Committees
- Committee members

Tables:

```text
committees
committee_members
```

---

## protocols

Responsibilities:

- Protocol lifecycle
- Protocol versions
- Document management

Tables:

```text
protocols
protocol_versions
documents
```

---

## reviews

Responsibilities:

- Reviewer assignment
- Review submission

Tables:

```text
review_assignments
reviews
```

---

## meetings

Responsibilities:

- Meeting scheduling
- Agenda management
- Voting

Tables:

```text
meetings
agenda_items
votes
```

---

## decisions

Responsibilities:

- Decisions
- Amendments

Tables:

```text
decisions
amendments
```

---

## monitoring

Responsibilities:

- Progress reports
- Adverse events
- Appeals

Tables:

```text
progress_reports
adverse_events
appeals
```

---

## workflow

Responsibilities:

- Workflow engine
- Rule validation
- State transitions

Tables:

```text
workflow_definitions
workflow_transitions
```

---

## notifications

Responsibilities:

- Email notifications
- In-app notifications

Tables:

```text
notifications
```

---

## audit

Responsibilities:

- Audit trail
- Event logging

Tables:

```text
audit_events
```

---

# 5. Internal Application Structure

Each application follows:

```text
app_name/
│
├── models/
├── api/
│   ├── serializers/
│   ├── views/
│   └── urls.py
│
├── services/
├── selectors/
├── permissions/
├── tasks/
└── tests/
```

---

# 6. Service Layer Pattern

Business logic must not be implemented inside:

- Views
- Serializers
- Models

Business logic belongs in services.

Example:

```python
ProtocolSubmissionService.submit(
    protocol=protocol,
    actor=user
)
```

Responsibilities:

- Validation
- Workflow execution
- Audit creation
- Notification dispatch

---

# 7. Selector Pattern

Selectors are read-only query services.

Example:

```python
ProtocolSelector.get_by_id()

ProtocolSelector.list_for_user()

MeetingSelector.upcoming()
```

Responsibilities:

- Query optimization
- Complex filtering
- Reusable read logic

---

# 8. Workflow Engine

Workflow is the source of truth.

Example:

```python
WorkflowEngine.transition(
    protocol,
    event="submit_protocol",
    actor=user
)
```

Execution Flow:

```text
Permission Check
        ↓
Rule Validation
        ↓
State Transition
        ↓
Audit Event
        ↓
Notifications
```

---

# 9. Rule Engine

Rules are isolated from workflow execution.

Example Rules:

```text
BR-001 Screening Completed

BR-002 Reviewer Assigned

BR-003 Quorum Met

BR-004 Decision Immutable
```

Example:

```python
RuleEngine.validate(
    protocol,
    event
)
```

---

# 10. Authorization Architecture

Authorization requires:

```text
Authentication
+
Tenant Validation
+
RBAC
+
Workflow Validation
+
Ownership Validation
+
Conflict Validation
```

Example:

```python
ReviewPermission.can_submit(
    user,
    protocol
)
```

---

# 11. Tenant Isolation

Tenant must be enforced on every query.

Example:

```python
Protocol.objects.filter(
    tenant_id=current_tenant
)
```

Cross-tenant access is prohibited.

---

# 12. Audit Architecture

Every important action generates an audit event.

Examples:

```text
Protocol Created

Protocol Submitted

Review Assigned

Vote Cast

Decision Published
```

Stored In:

```text
audit_events
```

---

# 13. Notification Architecture

Events trigger notifications.

Examples:

```text
Protocol Submitted

Review Assigned

Review Due Reminder

Decision Published
```

Channels:

```text
Email
In-App
```

---

# 14. Background Processing

Redis + Celery

Tasks:

```text
Email Sending

Notification Delivery

PDF Generation

Report Export

AI Analysis
```

Tasks must be asynchronous.

---

# 15. Document Storage

MVP:

```text
Local Storage
```

Production:

```text
S3-Compatible Storage
```

Requirements:

```text
UUID File Names

Access Control

Virus Scan Support
```

---

# 16. API Documentation

Generated Automatically Using:

```text
drf-spectacular
```

Available At:

```text
/api/schema/

/api/docs/

/api/redoc/
```

---

# 17. Testing Strategy

Required:

```text
Unit Tests

API Tests

Permission Tests

Workflow Tests
```

Coverage Target:

```text
80%+
```

---

# 18. Docker Architecture

Services:

```text
backend

postgres

redis

celery-worker

celery-beat
```

Development Startup:

```bash
docker compose up
```

---

# 19. MVP Scope

Included:

- Authentication
- User Management
- Protocol Management
- Reviews
- Meetings
- Decisions
- Workflow
- Audit Logging
- Notifications

Excluded:

- AI Assistance
- National Registry Integration
- Advanced Analytics
- Mobile Application

---

# 20. Definition of Done

Backend MVP is complete when:

- All database migrations succeed
- All workflow transitions function
- RBAC enforcement passes tests
- Audit logging is operational
- OpenAPI documentation is generated
- Docker deployment succeeds

---

# Freeze Status

Backend MVP Version: 1.0

Approved Inputs:

- architecture.md
- data-model.md
- workflow.md
- rbac.md
- database-schema.md
- api-spec.md

This specification is the implementation blueprint for the IRB backend.

---