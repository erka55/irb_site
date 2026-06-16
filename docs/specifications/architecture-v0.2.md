# IRB System Architecture Specification
Version: 0.2 (Refactored)
Status: Draft

---

# 1. System Vision

IRB (Institutional Review Board) систем нь судалгааны ёс зүйн хяналтын процессыг:

- Digitalized workflow-д шилжүүлэх
- Audit-able, compliance-ready болгох
- Event-driven процесс болгон загварчлах
- Multi-tenant байгууллагын платформ болгох
- AI-assisted decision support нэмэх (зөвхөн advisory)

зорилготой enterprise web platform юм.

---

# 2. Architectural Principles

Систем дараах үндсэн зарчмууд дээр тулгуурлана:

## 2.1 Event-Driven First
Бүх бизнес процесс event-үүдээр дамжин явна.

## 2.2 Workflow is Source of Truth
Workflow engine нь процессын цорын ганц truth layer байна.

## 2.3 Immutable Audit
Бүх үйлдэл event store дээр өөрчлөгдөшгүй хадгалагдана.

## 2.4 AI is Advisory Only
AI нь зөвхөн санал өгнө, шийдвэр гаргахгүй.

## 2.5 Multi-Tenant Isolation
Бүх өгөгдөл tenant-level isolation-той байна.

---

# 3. High-Level Architecture
```
[ Frontend Layer ]
↓
[ API Gateway (Thin Layer) ]
↓
[ Domain API Layer ]
↓
[ Workflow Orchestration Layer ]
↓
[ Domain Services Layer ]
↓
[ Event Bus ]
↓
[ Data Layer + Event Store + Storage ]
```

---

# 4. System Components

---

## 4.1 Frontend Layer

Tech stack:
- React / Next.js

Modules:
- PI Portal (Protocol submission)
- Reviewer Portal
- Chair Dashboard
- Admin Panel

Responsibilities:
- UI rendering
- Form submission
- Review workflow UI
- Notifications display

---

## 4.2 API Gateway (Thin Layer)

Responsibilities:
- Authentication verification (JWT)
- Rate limiting
- Request routing
- Basic request validation

NOT responsible for:
- Business logic
- RBAC decisions
- Workflow decisions

Endpoints:
- /auth/*
- /protocols/*
- /reviews/*
- /meetings/*
- /decisions/*

---

## 4.3 Domain API Layer

Responsibilities:
- Request orchestration
- Input validation
- Service composition
- Tenant context injection

This layer acts as a bridge between Gateway and Domain Services.

---

## 4.4 Workflow Orchestration Layer (Core Engine)

This is the HEART of the system.

Responsibilities:
- Workflow state transitions
- Process orchestration
- Approval chains
- Versioned workflow definitions
- Business rule evaluation

### Example Workflow States:
```
Event → Workflow Evaluation → Command → Domain Service → Event
```

---

## 4.5 Domain Services Layer

Pure business logic layer.

### Services:

#### Protocol Service
- Submission handling
- Versioning
- Document management

#### Review Service
- Reviewer assignment
- Review submission
- Scoring aggregation

#### Committee Service
- Meeting scheduling
- Agenda generation
- Voting system

#### Decision Service
- Final decision creation
- Letter generation
- Approval lifecycle

#### User Service
- Authentication support
- RBAC enforcement
- Tenant management

---

## 4.6 Event Bus

Technology:
- Kafka / RabbitMQ (recommended)

Responsibilities:
- Async communication
- Decoupling services
- Event propagation

### Example Events:

- ProtocolSubmitted
- ReviewAssigned
- ReviewCompleted
- MeetingScheduled
- DecisionIssued

---

## 4.7 Event Store (Audit Layer)

Immutable storage of all system events.

Purpose:
- Full audit trail
- Compliance requirement
- Replay capability
- Debugging & forensic analysis

---

## 4.8 Rules Engine (Embedded in Workflow Layer)

Handles business constraints:

- Conflict of interest checks
- Deadline enforcement
- Quorum validation
- State transition rules

Implementation:
- JSON-based rule definitions OR DSL

---

## 4.9 AI Assistance Layer (Async Advisory System)

AI is NOT part of core decision flow.

### Functions:

- Protocol quality analysis
- Reviewer suggestions
- Review summarization
- Decision letter draft generation

### Execution Model:
```
Event → AI Worker → Suggestion Output → Stored as advisory data
```

---

## 4.10 Data Layer

### Primary Database:
- PostgreSQL

### Cache:
- Redis (sessions, workflow state cache)

### Storage:
- S3-compatible object storage (documents)

### Event Store:
- Append-only event log storage

---

# 5. Multi-Tenancy Model

## Approach: Hybrid Model

- tenant_id in all tables (mandatory)
- PostgreSQL Row-Level Security (RLS)

### Isolation Guarantees:
- Data-level isolation
- Query-level enforcement
- Application-level context injection

---

# 6. Security Architecture

## 6.1 Authentication
- JWT-based auth
- Refresh token mechanism
- Optional MFA

## 6.2 Authorization Model

### RBAC:
- Role-based access control

### ABAC (State-based rules):
- Workflow state permissions
- Context-aware access rules

---

## 6.3 Audit System

Every action generates an immutable event:
- user
- action
- timestamp
- entity
- context

---

# 7. Workflow Execution Model
```
User Action
↓
Event Generated
↓
Workflow Engine Evaluates
↓
Business Rule Check
↓
Domain Service Execution
↓
New Event Emitted
↓
Side Effects Triggered
```

---

# 8. Side Effects System

Triggered asynchronously via Event Bus:

- Email notifications
- In-app notifications
- SMS (optional)
- AI processing jobs
- Report generation

---

# 9. Notifications System

Channels:
- Email
- In-app notifications
- SMS (optional)

Triggers:
- Submission received
- Review assigned
- Deadline warning
- Decision issued

---

# 10. Deployment Architecture
```
Frontend
↓
API Gateway
↓
Domain API Layer
↓
Workflow Orchestrator
↓
Domain Services
↓
Event Bus
↓
Workers (AI / Notifications / Email)
↓
Databases (PostgreSQL + Redis + Storage + Event Store)
```

---

# 11. Scalability Strategy

- Stateless services (horizontal scaling)
- Async processing via queue system
- Worker-based background jobs
- Cache optimization via Redis
- Event-driven decoupling

---

# 12. Observability

## Logging:
- Centralized logging (ELK stack)

## Metrics:
- Prometheus

## Tracing:
- OpenTelemetry

---

# 13. Critical Design Decisions

- Workflow is the single source of truth
- All actions are event-based
- Decision entities are immutable
- AI is advisory only
- Full audit trail is mandatory

---

# 14. Future Extensions

- National IRB integration
- Cross-institution review network
- Advanced AI ethics risk scoring
- Blockchain-based audit anchoring (optional)
- Fully automated pre-screening assistant

---
