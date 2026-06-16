# Repository Structure

Version: 1.0

Status: Final

---

# Purpose

This document defines:

* Git repository structure
* Branch strategy
* Environment management
* Commit conventions
* Docker layout
* Development workflow

for the IRB System backend.

---

# Repository Layout

```text
irb-system/

├── backend/
│
├── frontend/
│
├── docs/
│
├── deployment/
│
├── scripts/
│
├── .github/
│
├── .gitignore
│
├── README.md
│
└── docker-compose.yml
```

---

# Backend Layout

```text
backend/

├── manage.py
│
├── config/
│
├── apps/
│
├── common/
│
├── requirements/
│
├── media/
│
├── static/
│
├── logs/
│
├── tests/
│
└── docker/
```

---

# Frontend Layout

```text
frontend/

├── src/
├── public/
├── tests/
├── package.json
└── next.config.js
```

---

# Documentation Layout

```text
docs/

├── architecture/
│
├── backend/
│
├── frontend/
│
├── api/
│
├── database/
│
└── decisions/
```

Recommended files:

```text
docs/

architecture-v0.2.md
workflow-v1.0.md
rbac-v1.0.md
api-spec-v1.0.md

database/

erd-v1.1.md
database-schema-v1.1.md
django-model-mapping-v1.1.md

backend/

django-bootstrap-plan-v1.0.md
backend-implementation-plan-v1.0.md
```

---

# Branch Strategy

## Main

```text
main
```

Production-ready code only.

Protected branch.

---

## Development

```text
develop
```

Primary working branch.

All development merges here first.

---

## Feature Branches

Format:

```text
feature/<name>
```

Examples:

```text
feature/accounts

feature/protocols

feature/reviews

feature/workflow-engine
```

---

## Bug Fix Branches

```text
fix/<name>
```

Example:

```text
fix/jwt-authentication
```

---

# Initial Branch Setup

```bash
git checkout main

git checkout -b archive/pre-freeze

git push origin archive/pre-freeze

git checkout main

git checkout -b develop

git push origin develop
```

---

# Commit Convention

Format:

```text
type(scope): message
```

Examples:

```text
feat(accounts): add custom user model

feat(protocols): create protocol workflow

fix(reviews): reviewer assignment validation

docs(api): update protocol endpoints

refactor(workflow): extract state engine
```

---

# Allowed Commit Types

```text
feat

fix

docs

refactor

test

chore
```

---

# Environment Files

Never commit:

```text
.env

.env.local

.env.production
```

---

Repository includes:

```text
.env.example
```

---

# Example Environment Variables

```env
DEBUG=True

SECRET_KEY=

DATABASE_URL=

REDIS_URL=

JWT_SECRET=

AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_STORAGE_BUCKET_NAME=
```

---

# Git Ignore

Always ignore:

```text
venv/

.env

__pycache__/

*.pyc

db.sqlite3

media/

logs/

node_modules/

.next/
```

---

# Pull Request Rules

Before merge:

```text
Migration reviewed

Tests pass

Lint pass

API documentation updated
```

---

# Release Tags

Format:

```text
v1.0.0

v1.1.0

v1.2.0
```

---

# Development Workflow

```text
Issue
    ↓
Feature Branch
    ↓
Development
    ↓
Pull Request
    ↓
Develop
    ↓
Release
    ↓
Main
```

---

# Initial Repository Milestone

Milestone 1

```text
Project Bootstrap
```

Milestone 2

```text
Authentication + RBAC
```

Milestone 3

```text
Protocol Workflow
```

Milestone 4

```text
Review Workflow
```

Milestone 5

```text
Meeting + Decision
```

Milestone 6

```text
Monitoring + Notifications
```

---

# Final Notes

The repository structure supports:

* Django Backend
* Next.js Frontend
* PostgreSQL
* Redis
* Celery
* Docker
* CI/CD

and aligns with all approved architecture and schema specifications.

---
