# IRB Backend MVP Specification
Version: 0.1

---

# 1. Technology Stack

Framework:
- FastAPI

Database:
- PostgreSQL

ORM:
- SQLAlchemy 2.x

Migration:
- Alembic

Authentication:
- JWT

File Storage:
- MinIO / S3

Validation:
- Pydantic v2

---

# 2. Project Structure

backend/

├── app/
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── database.py
│   └── dependencies.py
│
├── models/
│
├── schemas/
│
├── repositories/
│
├── services/
│
├── api/
│
├── workflow/
│
├── audit/
│
├── notifications/
│
└── main.py

---

# 3. Domain Modules

## Auth Module

Responsibilities:

- login
- token generation
- current user

Endpoints:

POST /auth/login

GET /auth/me

---

## User Module

Responsibilities:

- user management
- role assignment

Endpoints:

GET /users

POST /users

GET /users/{id}

PUT /users/{id}

DELETE /users/{id}

---

## Protocol Module

Responsibilities:

- create protocol
- edit protocol
- submit protocol

Endpoints:

GET /protocols

POST /protocols

GET /protocols/{id}

PUT /protocols/{id}

POST /protocols/{id}/submit

---

## Review Module

Responsibilities:

- reviewer assignment
- review submission

Endpoints:

POST /protocols/{id}/assign-reviewer

POST /reviews

GET /reviews/{id}

---

## Decision Module

Responsibilities:

- approve
- reject
- issue decision

Endpoints:

POST /decisions

GET /protocols/{id}/decision

---

## Audit Module

Responsibilities:

- immutable audit trail

Endpoints:

GET /audit-logs