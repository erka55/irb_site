# Backend Implementation Plan

Version: 1.0

Status: Final

---

# Purpose

This document defines the implementation roadmap for the IRB Backend MVP.

Goal:

* Convert approved specifications into working code
* Minimize migration rework
* Establish stable development milestones

---

# Implementation Principles

## Principle 1

Database schema is source of truth.

Implementation must follow:

```text
ERD
    ↓
Database Schema
    ↓
Django Models
    ↓
API
```

Never reverse this order.

---

## Principle 2

Workflow drives business logic.

```text
UI
    ↓
API
    ↓
Workflow Engine
    ↓
Database
```

UI must not control workflow states directly.

---

## Principle 3

Services contain business logic.

Allowed:

```python
ProtocolService
ReviewService
DecisionService
```

Not allowed:

```python
views.py

serializers.py
```

---

# Phase 0 — Project Bootstrap

Duration:

```text
1–2 days
```

Tasks:

### Create Repository

```bash
git init
```

### Create Django Project

```bash
django-admin startproject config .
```

### Create Apps

```bash
accounts
committees
protocols
reviews
meetings
decisions
monitoring
notifications
audit
```

### Configure

```text
PostgreSQL

Redis

DRF

JWT

drf-spectacular
```

Deliverable:

```text
Project starts successfully
```

---

# Phase 1 — Foundation Layer

Priority:

```text
Highest
```

---

## accounts App

Implement:

```text
Tenant

User

Role

Permission

UserRole

RolePermission
```

Features:

```text
JWT Login

JWT Refresh

Role Assignment

Permission Checking
```

Deliverable:

```text
Authentication working
```

---

## audit App

Implement:

```text
AuditEvent
```

Create:

```python
AuditService
```

Auto-log:

```text
Protocol actions

Review actions

Decision actions
```

Deliverable:

```text
Audit trail working
```

---

# Phase 2 — Protocol Domain

Implement:

```text
Protocol

ProtocolVersion

Document

ProtocolComment

WorkflowHistory
```

---

## Services

Create:

```python
ProtocolService

WorkflowService
```

Functions:

```python
create_protocol()

submit_protocol()

create_version()

add_comment()
```

---

## Workflow Engine v1

States:

```text
DRAFT

SUBMITTED

SCREENING

REVIEW

MEETING

DECISION

ACTIVE

CLOSED
```

Deliverable:

```text
Protocol submission flow working
```

---

# Phase 3 — Review Domain

Implement:

```text
ReviewAssignment

Review
```

Services:

```python
ReviewService
```

Functions:

```python
assign_reviewer()

submit_review()

validate_conflict()
```

Deliverable:

```text
Reviewer workflow working
```

---

# Phase 4 — Committee Domain

Implement:

```text
Committee

CommitteeMember
```

Services:

```python
CommitteeService
```

Functions:

```python
create_committee()

add_member()

check_quorum()
```

Deliverable:

```text
Committee management working
```

---

# Phase 5 — Meeting Domain

Implement:

```text
Meeting

AgendaItem

Vote
```

Services:

```python
MeetingService
```

Functions:

```python
schedule_meeting()

generate_agenda()

record_vote()
```

Deliverable:

```text
Meeting workflow working
```

---

# Phase 6 — Decision Domain

Implement:

```text
Decision

Amendment
```

Services:

```python
DecisionService
```

Functions:

```python
issue_decision()

publish_decision()

create_amendment()
```

Rules:

```text
Published decisions immutable
```

Deliverable:

```text
Decision lifecycle working
```

---

# Phase 7 — Monitoring Domain

Implement:

```text
ProgressReport

AdverseEvent

Appeal
```

Deliverable:

```text
Post-approval monitoring working
```

---

# Phase 8 — Notification System

Implement:

```text
Notification
```

Channels:

```text
In-App

Email
```

Celery Tasks:

```python
send_email()

send_deadline_warning()

send_decision_notification()
```

Deliverable:

```text
Notification system working
```

---

# Phase 9 — API Stabilization

Implement:

```text
Filtering

Pagination

Permissions

Validation

Error Handling
```

Standard Response:

```json
{
  "success": true,
  "data": {}
}
```

Deliverable:

```text
Stable API v1
```

---

# Phase 10 — Testing

Coverage Targets:

```text
Models

Services

API

Workflow
```

Goal:

```text
≥ 80% coverage
```

Tools:

```text
pytest

pytest-django

factory-boy
```

---

# Migration Strategy

Migration Group 001

```text
accounts

audit
```

---

Migration Group 002

```text
committees
```

---

Migration Group 003

```text
protocols
```

---

Migration Group 004

```text
reviews
```

---

Migration Group 005

```text
meetings
```

---

Migration Group 006

```text
decisions
```

---

Migration Group 007

```text
monitoring

notifications
```

---

# MVP Completion Criteria

System must support:

```text
User Authentication

RBAC

Protocol Submission

Reviewer Assignment

Review Submission

Meeting Management

Voting

Decision Publication

Audit Logging

Notifications
```

---

# Success Definition

Backend MVP is complete when:

```text
All migrations run successfully

All core APIs documented

Workflow executes correctly

Audit trail generated

RBAC enforced

Test coverage >= 80%
```

---

# Next Document

After this plan:

```text
deployment-plan-v1.0.md
```

Then:

```text
Actual Django Development
```

---
