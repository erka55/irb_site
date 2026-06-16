# IRB System Architecture Specification
Version: 0.1
Status: Draft

---

# 1. System Vision

IRB систем нь судалгааны ёс зүйн хяналтын процессыг:

- Digitalize хийх
- Audit-able болгох
- Workflow-driven болгох
- AI-assisted review support нэмэх

зорилготой multi-tenant web platform байна.

---

# 2. High-Level Architecture

System is composed of 5 layers:

```
[ Frontend Layer ]
        ↓
[ API Gateway ]
        ↓
[ Application Services Layer ]
        ↓
[ Workflow Engine + Rules Engine ]
        ↓
[ Data Layer + File Storage ]
```

---

# 3. System Components

## 3.1 Frontend (Web App)

Tech suggestion:
- React / Next.js

Modules:
- PI Portal
- Reviewer Portal
- Chair Dashboard
- Admin Panel

Responsibilities:
- Form submission
- Review UI
- Meeting dashboard
- Notification display

---

## 3.2 API Gateway

Responsibilities:
- Authentication check
- Rate limiting
- Routing
- Role-based access enforcement

Endpoints exposed:
- /auth/*
- /protocols/*
- /reviews/*
- /meetings/*
- /decisions/*

---

## 3.3 Core Application Services

### 1. Protocol Service
- Submission lifecycle
- versioning
- document management

### 2. Review Service
- reviewer assignment
- review submission
- scoring aggregation

### 3. Committee Service
- meeting scheduling
- agenda generation
- voting system

### 4. Decision Service
- final decision creation
- approval lifecycle
- letter generation

### 5. User Service
- authentication
- RBAC
- institution management

---

## 3.4 Workflow Engine (Critical Component)

This is the heart of IRB system.

Responsibilities:
- State transitions
- Business rule validation
- Trigger automation

Example state machine:

```
Draft → Submitted → Screening → Review → Meeting → Decision → Active
```

Rules engine checks:

- completeness
- reviewer conflict
- quorum
- deadlines

---

## 3.5 Rules Engine

Handles:

- BR-001 conflict of interest
- BR-002 deadline enforcement
- BR-003 quorum validation
- BR-004 approval immutability

Implementation idea:
- Rule DSL or JSON-based rules

---

## 3.6 AI Assistance Layer (Optional but powerful)

AI functions:

### 1. Protocol Quality Check
- missing sections detection
- ethics risk estimation

### 2. Reviewer Suggestion
- match reviewer expertise

### 3. Review Summarization
- summarize long reviews

### 4. Decision Drafting
- generate decision letter draft

---

## 3.7 Data Layer

### Database:
- PostgreSQL (primary relational store)

### Storage:
- S3-compatible object storage (documents)

### Cache:
- Redis (workflow state, sessions)

---

# 4. Deployment Architecture

```
           [ Load Balancer ]
                   |
        -------------------------
        |                       |
 [ Web Frontend ]      [ API Backend Cluster ]
                              |
              --------------------------------
              |              |               |
      Protocol Service  Review Service  Committee Service
              |
       Workflow Engine
              |
        PostgreSQL + Redis + Storage
```

---

# 5. Multi-Tenancy Model

Each institution has isolated:

- Users
- Protocols
- Reviews
- Meetings

Approach:

- tenant_id in all tables
OR
- schema-based isolation (advanced)

---

# 6. Security Architecture

## Authentication
- JWT + Refresh token
- Optional MFA

## Authorization
- RBAC (role-based)
- state-based permissions (ABAC layer)

## Audit
- immutable audit log
- full trace of:
  - who
  - what
  - when

---

# 7. Workflow Execution Model

Workflow engine uses:

```
Event → Rule Check → State Transition → Side Effects
```

Side effects:
- notification
- email
- logging
- AI processing trigger

---

# 8. Notifications System

Channels:
- Email
- In-app
- SMS (optional)

Events:
- submission received
- review assigned
- deadline warning
- decision issued

---

# 9. Scalability Considerations

- Stateless API services
- Horizontal scaling
- Async processing (queue-based)
- Background workers for:
  - email
  - AI processing
  - report generation

Suggested:
- RabbitMQ / Kafka

---

# 10. Observability

- Logging: centralized (ELK stack)
- Metrics: Prometheus
- Tracing: OpenTelemetry

---

# 11. Critical Design Decisions

### 1. Workflow is source of truth
System logic is driven by workflow engine, not UI.

### 2. Decision is immutable
Once issued → cannot be edited

### 3. Every action is audited
No exception

### 4. AI is advisory only
Never overrides human decision

---

# 12. Future Extensions

- National IRB registry integration
- Cross-institution review
- Blockchain-based audit trail (optional)
- Fully automated ethics pre-screening AI