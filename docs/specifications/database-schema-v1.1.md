# Database Schema Specification

Version: 1.1
Status: Final

---

# Protocol Domain

## protocols

```sql
CREATE TABLE protocols (

    id UUID PRIMARY KEY,

    tenant_id UUID NOT NULL,

    protocol_number VARCHAR(100) NOT NULL,

    title VARCHAR(500) NOT NULL,

    principal_investigator_id UUID NOT NULL,

    workflow_state VARCHAR(50) NOT NULL,

    current_version_id UUID NULL,

    submitted_at TIMESTAMPTZ NULL,

    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    deleted_at TIMESTAMPTZ NULL,

    created_at TIMESTAMPTZ NOT NULL,

    updated_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_protocol_tenant
        FOREIGN KEY (tenant_id)
        REFERENCES tenants(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_protocol_pi
        FOREIGN KEY (principal_investigator_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
);
```

Indexes

```sql
CREATE INDEX idx_protocols_tenant
ON protocols(tenant_id);

CREATE INDEX idx_protocols_state
ON protocols(workflow_state);

CREATE INDEX idx_protocols_number
ON protocols(protocol_number);

CREATE INDEX idx_protocols_submitted
ON protocols(submitted_at);
```

---

## protocol_versions

```sql
CREATE TABLE protocol_versions (

    id UUID PRIMARY KEY,

    protocol_id UUID NOT NULL,

    version_no INTEGER NOT NULL,

    summary TEXT,

    change_notes TEXT,

    created_at TIMESTAMPTZ NOT NULL,

    updated_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_protocol_version_protocol
        FOREIGN KEY (protocol_id)
        REFERENCES protocols(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_protocol_version
        UNIQUE(protocol_id, version_no)
);
```

---

## documents

```sql
CREATE TABLE documents (

    id UUID PRIMARY KEY,

    protocol_version_id UUID NOT NULL,

    document_type VARCHAR(100) NOT NULL,

    file_name VARCHAR(500) NOT NULL,

    file_path VARCHAR(1000) NOT NULL,

    file_size BIGINT,

    mime_type VARCHAR(255),

    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    deleted_at TIMESTAMPTZ NULL,

    created_at TIMESTAMPTZ NOT NULL,

    updated_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_document_version
        FOREIGN KEY (protocol_version_id)
        REFERENCES protocol_versions(id)
        ON DELETE CASCADE
);
```

---

## protocol_comments

```sql
CREATE TABLE protocol_comments (

    id UUID PRIMARY KEY,

    protocol_id UUID NOT NULL,

    author_id UUID NOT NULL,

    comment_type VARCHAR(50) NOT NULL,

    comment_text TEXT NOT NULL,

    is_internal BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_comment_protocol
        FOREIGN KEY (protocol_id)
        REFERENCES protocols(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_comment_author
        FOREIGN KEY (author_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
);
```

---

## workflow_histories

```sql
CREATE TABLE workflow_histories (

    id UUID PRIMARY KEY,

    protocol_id UUID NOT NULL,

    from_state VARCHAR(50),

    to_state VARCHAR(50) NOT NULL,

    event VARCHAR(100) NOT NULL,

    performed_by UUID NOT NULL,

    performed_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_wh_protocol
        FOREIGN KEY (protocol_id)
        REFERENCES protocols(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_wh_user
        FOREIGN KEY (performed_by)
        REFERENCES users(id)
        ON DELETE RESTRICT
);
```

Indexes

```sql
CREATE INDEX idx_wh_protocol
ON workflow_histories(protocol_id);

CREATE INDEX idx_wh_performed_at
ON workflow_histories(performed_at);
```

---

# Review Domain

## review_assignments

```sql
CREATE TABLE review_assignments (

    id UUID PRIMARY KEY,

    protocol_id UUID NOT NULL,

    reviewer_id UUID NOT NULL,

    assigned_at TIMESTAMPTZ NOT NULL,

    due_date DATE,

    status VARCHAR(50) NOT NULL,

    CONSTRAINT fk_ra_protocol
        FOREIGN KEY (protocol_id)
        REFERENCES protocols(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_ra_reviewer
        FOREIGN KEY (reviewer_id)
        REFERENCES users(id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_ra_protocol_reviewer
        UNIQUE(protocol_id, reviewer_id)
);
```

---

## reviews

```sql
CREATE TABLE reviews (

    id UUID PRIMARY KEY,

    assignment_id UUID NOT NULL UNIQUE,

    recommendation VARCHAR(50) NOT NULL,

    comments TEXT,

    submitted_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL,

    updated_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_review_assignment
        FOREIGN KEY (assignment_id)
        REFERENCES review_assignments(id)
        ON DELETE CASCADE
);
```

Index

```sql
CREATE INDEX idx_reviews_submitted
ON reviews(submitted_at);
```

---

# Meeting Domain

## meetings

```sql
CREATE TABLE meetings (

    id UUID PRIMARY KEY,

    committee_id UUID NOT NULL,

    meeting_date DATE NOT NULL,

    location VARCHAR(255),

    status VARCHAR(50) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL,

    updated_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_meeting_committee
        FOREIGN KEY (committee_id)
        REFERENCES committees(id)
        ON DELETE RESTRICT
);
```

---

## agenda_items

```sql
CREATE TABLE agenda_items (

    id UUID PRIMARY KEY,

    meeting_id UUID NOT NULL,

    protocol_id UUID NOT NULL,

    sequence_no INTEGER NOT NULL,

    CONSTRAINT fk_agenda_meeting
        FOREIGN KEY (meeting_id)
        REFERENCES meetings(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_agenda_protocol
        FOREIGN KEY (protocol_id)
        REFERENCES protocols(id)
        ON DELETE RESTRICT
);
```

---

## votes

```sql
CREATE TABLE votes (

    id UUID PRIMARY KEY,

    agenda_item_id UUID NOT NULL,

    voter_id UUID NOT NULL,

    vote VARCHAR(50) NOT NULL,

    comments TEXT,

    created_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_vote_agenda
        FOREIGN KEY (agenda_item_id)
        REFERENCES agenda_items(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_vote_user
        FOREIGN KEY (voter_id)
        REFERENCES users(id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_vote
        UNIQUE(agenda_item_id, voter_id)
);
```

---

# Decision Domain

## decisions

```sql
CREATE TABLE decisions (

    id UUID PRIMARY KEY,

    protocol_id UUID NOT NULL,

    decision_type VARCHAR(50) NOT NULL,

    decision_text TEXT NOT NULL,

    metadata JSONB NULL,

    issued_at TIMESTAMPTZ NOT NULL,

    published_at TIMESTAMPTZ NULL,

    created_at TIMESTAMPTZ NOT NULL,

    updated_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_decision_protocol
        FOREIGN KEY (protocol_id)
        REFERENCES protocols(id)
        ON DELETE RESTRICT
);
```

Index

```sql
CREATE INDEX idx_decisions_issued
ON decisions(issued_at);
```

Business Rule

```text
Published decisions are immutable.
Physical delete is prohibited.
```

---

## amendments

```sql
CREATE TABLE amendments (

    id UUID PRIMARY KEY,

    protocol_id UUID NOT NULL,

    amendment_type VARCHAR(100) NOT NULL,

    description TEXT,

    submitted_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_amendment_protocol
        FOREIGN KEY (protocol_id)
        REFERENCES protocols(id)
        ON DELETE RESTRICT
);
```

---

# Monitoring Domain

## progress_reports

```sql
CREATE TABLE progress_reports (

    id UUID PRIMARY KEY,

    protocol_id UUID NOT NULL,

    report_period VARCHAR(100),

    summary TEXT,

    submitted_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_progress_protocol
        FOREIGN KEY (protocol_id)
        REFERENCES protocols(id)
        ON DELETE RESTRICT
);
```

---

## adverse_events

```sql
CREATE TABLE adverse_events (

    id UUID PRIMARY KEY,

    protocol_id UUID NOT NULL,

    event_date DATE NOT NULL,

    severity VARCHAR(50),

    description TEXT,

    created_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_adverse_protocol
        FOREIGN KEY (protocol_id)
        REFERENCES protocols(id)
        ON DELETE RESTRICT
);
```

---

## appeals

```sql
CREATE TABLE appeals (

    id UUID PRIMARY KEY,

    protocol_id UUID NOT NULL,

    reason TEXT NOT NULL,

    submitted_at TIMESTAMPTZ NOT NULL,

    status VARCHAR(50) NOT NULL,

    CONSTRAINT fk_appeal_protocol
        FOREIGN KEY (protocol_id)
        REFERENCES protocols(id)
        ON DELETE RESTRICT
);
```

---

# Notification Domain

## notifications

```sql
CREATE TABLE notifications (

    id UUID PRIMARY KEY,

    user_id UUID NOT NULL,

    title VARCHAR(255) NOT NULL,

    message TEXT NOT NULL,

    is_read BOOLEAN NOT NULL DEFAULT FALSE,

    read_at TIMESTAMPTZ NULL,

    created_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_notification_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
);
```

Indexes

```sql
CREATE INDEX idx_notifications_user
ON notifications(user_id);

CREATE INDEX idx_notifications_read
ON notifications(is_read);
```

---

# Audit Domain

## audit_events

```sql
CREATE TABLE audit_events (

    id UUID PRIMARY KEY,

    actor_id UUID NOT NULL,

    entity_type VARCHAR(100) NOT NULL,

    entity_id UUID NOT NULL,

    action VARCHAR(100) NOT NULL,

    payload JSONB,

    created_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_audit_actor
        FOREIGN KEY (actor_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
);
```

Indexes

```sql
CREATE INDEX idx_audit_entity
ON audit_events(entity_type, entity_id);

CREATE INDEX idx_audit_actor
ON audit_events(actor_id);

CREATE INDEX idx_audit_created
ON audit_events(created_at);
```

Business Rule

```text
Audit records are immutable.
Audit records are never physically deleted.
```

---

# Final Schema Rules

* UUID primary keys for all tables
* Multi-tenant isolation enforced
* Protocols use soft delete
* Decisions are immutable after publication
* Audit records are immutable
* Workflow transitions recorded in workflow_histories
* All timestamps use TIMESTAMPTZ
* PostgreSQL is the authoritative database engine

---
