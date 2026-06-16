# Django Bootstrap Plan

Version: 1.0
Status: Final

---

# Purpose

This document defines the initial Django project setup for the IRB System.

It provides:

* Project structure
* Technology stack
* Configuration strategy
* Deployment foundation
* Development conventions

This document is the implementation blueprint for the backend MVP.

---

# Technology Stack

## Backend Framework

```text
Python 3.13+
Django 5.x
Django REST Framework
```

---

## Database

```text
PostgreSQL 18+
```

Encoding:

```text
UTF-8
```

Timezone:

```text
UTC
```

---

## Cache

```text
Redis
```

Used for:

* caching
* Celery broker
* session storage (optional)

---

## Background Processing

```text
Celery
```

Tasks:

* Email notifications
* Report generation
* AI processing
* Scheduled reminders

---

## Authentication

```text
JWT
```

Library:

```text
djangorestframework-simplejwt
```

---

## Object Storage

```text
S3 Compatible Storage
```

Options:

```text
MinIO
AWS S3
Cloudflare R2
```

---

## API Documentation

```text
drf-spectacular
```

Provides:

```text
OpenAPI 3
Swagger UI
ReDoc
```

---

## Containerization

```text
Docker
Docker Compose
```

---

# Project Structure

```text
irb_backend/

├── manage.py

├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   ├── test.py
│   │   └── production.py
│   │
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│   ├── accounts/
│   ├── committees/
│   ├── protocols/
│   ├── reviews/
│   ├── meetings/
│   ├── decisions/
│   ├── monitoring/
│   ├── notifications/
│   └── audit/
│
├── common/
│   ├── models/
│   ├── permissions/
│   ├── services/
│   ├── exceptions/
│   ├── middleware/
│   └── utils/
│
├── media/
├── static/
│
├── logs/
│
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
│
└── docker/
```

---

# Settings Strategy

## base.py

Contains:

```text
INSTALLED_APPS

MIDDLEWARE

REST_FRAMEWORK

DATABASES

AUTH_USER_MODEL

LANGUAGE_CODE

TIME_ZONE
```

---

## local.py

Development environment.

```text
DEBUG = True
```

---

## production.py

Production environment.

```text
DEBUG = False

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
```

---

# Installed Apps

## Django

```text
django.contrib.admin
django.contrib.auth
django.contrib.contenttypes
django.contrib.sessions
django.contrib.messages
django.contrib.staticfiles
```

---

## Third Party

```text
rest_framework

rest_framework_simplejwt

drf_spectacular

django_filters

storages

corsheaders
```

---

## Local Apps

```text
apps.accounts

apps.committees

apps.protocols

apps.reviews

apps.meetings

apps.decisions

apps.monitoring

apps.notifications

apps.audit
```

---

# Authentication Strategy

Custom user model.

```python
AUTH_USER_MODEL = "accounts.User"
```

Authentication:

```text
JWT Access Token

JWT Refresh Token
```

RBAC enforced via:

```text
Role

Permission

RolePermission

UserRole
```

---

# API Structure

Versioned API.

```text
/api/v1/
```

Example:

```text
/api/v1/auth/

/api/v1/protocols/

/api/v1/reviews/

/api/v1/meetings/

/api/v1/decisions/
```

---

# Application Layer Pattern

Each app follows:

```text
models.py

serializers.py

views.py

services.py

permissions.py

selectors.py

urls.py
```

---

# Service Layer Rule

Business logic must not live in:

```text
views.py

serializers.py
```

Business logic belongs in:

```text
services.py
```

Example:

```python
ProtocolService.submit()

ReviewService.assign_reviewer()

DecisionService.publish()
```

---

# Workflow Engine Strategy

Location:

```text
apps/protocols/workflows/
```

Structure:

```text
states.py

events.py

rules.py

engine.py
```

Workflow flow:

```text
Event
    ↓
Rule Validation
    ↓
State Transition
    ↓
WorkflowHistory
    ↓
Notifications
```

---

# File Storage Strategy

Files are never stored in database.

Database stores:

```text
file_name

file_path

file_size

mime_type
```

Physical storage:

```text
S3 bucket
```

Path example:

```text
tenant-id/

protocol-id/

version/

document.pdf
```

---

# Logging Strategy

Log format:

```text
JSON
```

Log categories:

```text
application

security

workflow

audit
```

Directory:

```text
logs/
```

---

# Audit Strategy

Every critical action creates:

```text
AuditEvent
```

Examples:

```text
Protocol Submitted

Reviewer Assigned

Review Submitted

Decision Published

Role Changed
```

---

# Celery Structure

```text
config/celery.py

apps/
    notifications/tasks.py
    decisions/tasks.py
    protocols/tasks.py
```

Queue examples:

```text
email

reports

ai

default
```

---

# Security Requirements

## Authentication

```text
JWT
```

---

## Authorization

```text
RBAC
```

and

```text
Workflow State Permission
```

---

## Passwords

```text
Argon2
```

preferred.

---

## HTTPS

Mandatory in production.

---

# Docker Structure

```text
docker/

├── django/
│   └── Dockerfile
│
├── nginx/
│   └── nginx.conf
│
└── compose/
    ├── local.yml
    └── production.yml
```

---

# Initial Development Order

Phase 1

```text
accounts

committees

protocols
```

---

Phase 2

```text
reviews

meetings

decisions
```

---

Phase 3

```text
monitoring

notifications

audit
```

---

# MVP Definition

MVP must support:

```text
User Authentication

RBAC

Protocol Submission

Reviewer Assignment

Review Submission

Meeting Agenda

Voting

Decision Publication

Audit Logging
```

---

# Final Freeze Notes

This bootstrap plan is aligned with:

* architecture-v0.2.md
* workflow-v1.0.md
* rbac-v1.0.md
* api-spec-v1.0.md
* erd-v1.1.md
* database-schema-v1.1.md
* django-model-mapping-v1.1.md

This document serves as the implementation blueprint for the Django backend MVP.

---
