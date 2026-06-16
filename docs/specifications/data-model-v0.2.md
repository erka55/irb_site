# IRB System Data Model Specification
Version: 0.1
Status: Draft

---

# 1. Purpose

This document defines the conceptual data model of the IRB System.

The model serves as the foundation for:

- Database schema design
- API specification
- Workflow implementation
- RBAC authorization
- Audit and compliance mechanisms

---

# 2. Design Principles

## 2.1 Tenant Isolation

All business entities belong to exactly one tenant.

Every major entity contains:

- tenant_id

---

## 2.2 Auditability

All critical actions generate audit events.

Every major entity must support:

- created_at
- created_by
- updated_at
- updated_by

---

## 2.3 Workflow-Driven Model

Protocol lifecycle is controlled by workflow state.

State transitions are managed by Workflow Engine.

---

## 2.4 Version Preservation

Research protocols are versioned.

Historical versions must never be overwritten.

---

# 3. Core Domain Entities

---

# 3.1 Tenant

Represents an institution.

Attributes:

- id
- name
- code
- status
- created_at

Relationships:

- Tenant → Users
- Tenant → Committees
- Tenant → Protocols

Cardinality:

```text
Tenant 1 --- N User
Tenant 1 --- N Committee
Tenant 1 --- N Protocol
```

---

# 3.2 User

Represents a system user.

Attributes:

- id
- tenant_id
- email
- first_name
- last_name
- title
- status

Relationships:

- User submits Protocols
- User reviews Protocols
- User participates in Meetings

---

# 3.3 Role

System role definition.

Examples:

- PI
- CoInvestigator
- Reviewer
- Chair
- Secretary
- Admin

Relationship:

```text
User N --- M Role
```

---

# 3.4 Committee

IRB committee.

Attributes:

- id
- tenant_id
- name
- description
- active

Relationships:

- Committee has Members
- Committee conducts Meetings

---

# 3.5 CommitteeMember

Links users to committees.

Attributes:

- committee_id
- user_id
- role_in_committee

Examples:

- Chair
- Vice Chair
- Member
- Community Representative

---

# 4. Protocol Domain

---

# 4.1 Protocol

Primary research submission.

Attributes:

- id
- tenant_id
- protocol_number
- title
- principal_investigator_id
- workflow_state
- submission_type
- review_type
- created_at

Relationships:

- Protocol has Versions
- Protocol has Reviews
- Protocol has Decisions
- Protocol has Documents

---

# 4.2 ProtocolVersion

Immutable version of protocol.

Attributes:

- id
- protocol_id
- version_number
- status
- submitted_at

Relationship:

```text
Protocol 1 --- N ProtocolVersion
```

---

# 4.3 Document

Uploaded document.

Examples:

- Proposal
- Consent Form
- Questionnaire
- Risk Assessment
- Data Protection Plan

Attributes:

- id
- protocol_version_id
- document_type
- storage_path
- uploaded_at

Relationship:

```text
ProtocolVersion 1 --- N Document
```

---

# 5. Review Domain

---

# 5.1 ReviewAssignment

Assigns reviewer to protocol.

Attributes:

- id
- protocol_id
- reviewer_id
- assigned_date
- due_date
- status

Relationship:

```text
Protocol 1 --- N ReviewAssignment
User 1 --- N ReviewAssignment
```

---

# 5.2 Review

Reviewer's evaluation.

Attributes:

- id
- assignment_id
- recommendation
- comments
- submitted_at

Recommendations:

- Approve
- Conditional Approve
- Request Information
- Reject

Relationship:

```text
ReviewAssignment 1 --- 1 Review
```

---

# 6. Meeting Domain

---

# 6.1 Meeting

Committee meeting.

Attributes:

- id
- committee_id
- meeting_date
- quorum_required
- status

Relationship:

```text
Committee 1 --- N Meeting
```

---

# 6.2 AgendaItem

Protocol discussed in meeting.

Attributes:

- id
- meeting_id
- protocol_id
- order_number

Relationship:

```text
Meeting 1 --- N AgendaItem
Protocol 1 --- N AgendaItem
```

---

# 6.3 Vote

Committee member vote.

Attributes:

- id
- agenda_item_id
- voter_id
- vote

Vote Values:

- Approve
- Reject
- Abstain

Relationship:

```text
AgendaItem 1 --- N Vote
```

---

# 7. Decision Domain

---

# 7.1 Decision

Official IRB decision.

Attributes:

- id
- protocol_id
- decision_type
- decision_date
- effective_date

Decision Types:

- Approved
- Conditional Approval
- Additional Information Required
- Rejected

Relationship:

```text
Protocol 1 --- N Decision
```

---

# 7.2 Amendment

Protocol amendment request.

Attributes:

- id
- protocol_id
- amendment_type
- description
- status

Relationship:

```text
Protocol 1 --- N Amendment
```

---

# 8. Monitoring Domain

---

# 8.1 ProgressReport

Periodic progress update.

Attributes:

- id
- protocol_id
- report_period
- summary
- submitted_at

Relationship:

```text
Protocol 1 --- N ProgressReport
```

---

# 8.2 AdverseEvent

Unexpected incident report.

Attributes:

- id
- protocol_id
- severity
- description
- reported_at

Relationship:

```text
Protocol 1 --- N AdverseEvent
```

---

# 9. Appeals Domain

---

# 9.1 Appeal

Decision appeal request.

Attributes:

- id
- protocol_id
- appellant_id
- appeal_reason
- submitted_at
- status

Relationship:

```text
Protocol 1 --- N Appeal
```

---

# 10. Conflict of Interest Domain

---

# 10.1 ConflictDeclaration

Conflict of interest disclosure.

Attributes:

- id
- user_id
- protocol_id
- declaration_type
- description
- declared_at

Relationship:

```text
User 1 --- N ConflictDeclaration
Protocol 1 --- N ConflictDeclaration
```

---

# 11. Notification Domain

---

# 11.1 Notification

System notification.

Attributes:

- id
- user_id
- channel
- subject
- message
- sent_at

Relationship:

```text
User 1 --- N Notification
```

---

# 12. Audit Domain

---

# 12.1 AuditEvent

Immutable audit log.

Attributes:

- id
- tenant_id
- actor_id
- entity_type
- entity_id
- action
- timestamp
- payload

Examples:

- ProtocolSubmitted
- ReviewAssigned
- DecisionIssued
- AmendmentApproved

Relationship:

```text
All major entities
    ↓
AuditEvent
```

---

# 13. Entity Relationship Summary

```text
Tenant
 ├── User
 ├── Committee
 └── Protocol
        ├── ProtocolVersion
        │      └── Document
        │
        ├── ReviewAssignment
        │      └── Review
        │
        ├── Decision
        ├── Amendment
        ├── ProgressReport
        ├── AdverseEvent
        ├── Appeal
        │
        └── AgendaItem
                 ↑
              Meeting
                 ↑
             Committee

User
 ├── Vote
 ├── Notification
 ├── ConflictDeclaration
 └── AuditEvent
```

---