# IRB System Implementation Roadmap
Version: 0.1

Goal:
Build a working IRB MVP system (Web-based) in 8 weeks.

Stack:
- FastAPI
- PostgreSQL
- Next.js
- Docker

---

# Phase 0: Project Setup (Week 1)

## Goals
Project skeleton + infrastructure бэлдэх

## Tasks

### Backend Setup
- FastAPI project init
- Folder structure setup
- PostgreSQL connection
- Alembic init
- JWT auth skeleton

### Frontend Setup
- Next.js project init
- Tailwind setup
- Layout structure
- Auth pages (UI only)

### DevOps
- Docker compose (backend + db + frontend)
- Environment config (.env)

## Deliverable
- Running empty system:
  - frontend loads
  - backend responds
  - database connected

---

# Phase 1: Core Identity System (Week 2)

## Goals
User authentication + RBAC

## Backend
- User model
- Role model
- JWT login/logout
- Password hashing
- RBAC middleware

## Frontend
- Login page
- Protected routes
- Role-based navigation

## Deliverable
- Users can login
- Role-based access works

---

# Phase 2: Protocol Core (Week 3)

## Goals
IRB protocol CRUD system

## Backend
- Protocol model
- Create / update / get
- Draft system
- Submit endpoint
- File upload (basic)

## Frontend
- PI dashboard
- Create protocol form
- Protocol list
- Protocol detail page

## Deliverable
- PI can create & submit protocol

---

# Phase 3: Review System (Week 4)

## Goals
Reviewer workflow

## Backend
- ReviewAssignment model
- Assign reviewer endpoint
- Review submission API
- Validation rules

## Frontend
- Reviewer dashboard
- Review form
- Assigned protocols list

## Deliverable
- Reviewer can submit review

---

# Phase 4: Workflow Engine (Week 5)

## Goals
State machine implementation

## Backend
- Workflow service
- State transitions
- Validation rules (invalid transitions blocked)
- Workflow history table

## Frontend
- Status badges
- Protocol state tracking UI
- Chair dashboard basic view

## Deliverable
- End-to-end lifecycle works:
  Draft → Submitted → Review

---

# Phase 5: Decision System (Week 6)

## Goals
Final IRB decision system

## Backend
- Decision model
- Committee meeting model
- Decision creation API
- Approval / rejection logic

## Frontend
- Chair dashboard
- Decision screen
- Protocol summary view

## Deliverable
- Full approval workflow works

---

# Phase 6: Audit + Notifications (Week 7)

## Goals
Traceability + communication

## Backend
- Audit log service
- Email queue system
- Notification service

## Frontend
- Audit log viewer (Admin)
- Notification UI

## Deliverable
- All actions tracked
- Emails generated

---

# Phase 7: Polish + Stabilization (Week 8)

## Goals
Production-ready MVP

## Tasks

### Backend
- Bug fixes
- Validation hardening
- Performance tuning

### Frontend
- UI cleanup
- UX improvements
- Form validation polish

### DevOps
- Production Docker build
- Deployment config

## Deliverable
- MVP production deployable system

---

# Definition of Done (MVP)

System is complete when:

✔ User can register/login  
✔ PI can create protocol  
✔ PI can submit protocol  
✔ Reviewer can review  
✔ Chair can make decision  
✔ Workflow transitions correctly  
✔ Audit logs exist  
✔ Notifications work  
✔ System runs in Docker  

---

# Post-MVP (Future)

- AI protocol review assistant
- Risk scoring engine
- Multi-institution support
- Advanced reporting dashboard
- Mobile app