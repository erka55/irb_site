# IRB RBAC (Role-Based Access Control)

Version: 0.2  
Status: Draft

---

# 1. Purpose

This document defines authorization rules for the IRB System.

Authorization is based on:

- RBAC (Role-Based Access Control)
- ABAC (Attribute-Based Access Control)
- Workflow State Restrictions
- Tenant Isolation

---

# 2. Authorization Model

The system uses a hybrid model:

```text
Authentication
        ↓
Tenant Validation
        ↓
Role Permission Check (RBAC)
        ↓
Workflow State Check (ABAC)
        ↓
Resource Ownership Check
```

---

# 3. System Roles

## 3.1 Admin

Responsibilities:

- Tenant administration
- User management
- Role assignment
- System configuration

Scope:

- All resources within tenant

---

## 3.2 Chair

Responsibilities:

- Committee leadership
- Reviewer assignment approval
- Meeting management
- Final decision approval

Scope:

- All committee protocols

---

## 3.3 Secretary

Responsibilities:

- Intake screening
- Workflow coordination
- Meeting scheduling
- Communication management

Scope:

- Administrative access without decision authority

---

## 3.4 Reviewer

Responsibilities:

- Review assigned protocols
- Submit recommendations
- Participate in voting

Scope:

- Assigned protocols only

---

## 3.5 PI (Principal Investigator)

Responsibilities:

- Create submissions
- Submit amendments
- Submit reports
- Respond to requests

Scope:

- Own protocols only

---

## 3.6 Co-Investigator

Responsibilities:

- Collaborate on protocol preparation

Scope:

- Assigned protocols only

---

# 4. Resource Types

- Protocol
- ProtocolVersion
- Document
- ReviewAssignment
- Review
- Meeting
- AgendaItem
- Vote
- Decision
- Amendment
- ProgressReport
- AdverseEvent
- Appeal
- Notification
- AuditEvent

---

# 5. Protocol Permissions

| Action | PI | Co-I | Reviewer | Secretary | Chair | Admin |
|----------|-----|------|----------|-----------|-------|-------|
| Create | ✔ | ✖ | ✖ | ✖ | ✖ | ✔ |
| View | Own | Assigned | Assigned | All | All | All |
| Edit Draft | Own | Assigned | ✖ | ✖ | ✖ | ✔ |
| Submit | ✔ | ✖ | ✖ | ✖ | ✖ | ✔ |
| Withdraw | Own | ✖ | ✖ | ✔ | ✔ | ✔ |

---

# 6. Document Permissions

| Action | PI | Co-I | Reviewer | Secretary | Chair | Admin |
|----------|-----|------|----------|-----------|-------|-------|
| Upload | ✔ | ✔ | ✖ | ✖ | ✖ | ✔ |
| View | Own | Assigned | Assigned | All | All | All |
| Delete Draft | Own | ✖ | ✖ | ✖ | ✖ | ✔ |

---

# 7. Review Permissions

| Action | PI | Co-I | Reviewer | Secretary | Chair | Admin |
|----------|-----|------|----------|-----------|-------|-------|
| Assign Reviewer | ✖ | ✖ | ✖ | ✔ | ✔ | ✔ |
| View Assignment | ✖ | ✖ | Own | All | All | All |
| Create Review | ✖ | ✖ | ✔ | ✖ | ✔ | ✔ |
| Edit Review | ✖ | ✖ | Own | ✖ | ✔ | ✔ |
| Submit Review | ✖ | ✖ | ✔ | ✖ | ✔ | ✔ |

---

# 8. Meeting Permissions

| Action | PI | Co-I | Reviewer | Secretary | Chair | Admin |
|----------|-----|------|----------|-----------|-------|-------|
| Create Meeting | ✖ | ✖ | ✖ | ✔ | ✔ | ✔ |
| Edit Meeting | ✖ | ✖ | ✖ | ✔ | ✔ | ✔ |
| View Meeting | ✖ | ✖ | Assigned | ✔ | ✔ | ✔ |

---

# 9. Voting Permissions

| Action | PI | Co-I | Reviewer | Secretary | Chair | Admin |
|----------|-----|------|----------|-----------|-------|-------|
| Vote | ✖ | ✖ | ✔ | ✖ | ✔ | ✔ |
| View Votes | ✖ | ✖ | Own | ✔ | ✔ | ✔ |

---

# 10. Decision Permissions

| Action | PI | Co-I | Reviewer | Secretary | Chair | Admin |
|----------|-----|------|----------|-----------|-------|-------|
| Create | ✖ | ✖ | ✖ | ✖ | ✔ | ✔ |
| Approve | ✖ | ✖ | ✖ | ✖ | ✔ | ✔ |
| Publish | ✖ | ✖ | ✖ | ✔ | ✔ | ✔ |
| View | Own | Assigned | Assigned | All | All | All |

---

# 11. Amendment Permissions

| Action | PI | Co-I | Reviewer | Secretary | Chair | Admin |
|----------|-----|------|----------|-----------|-------|-------|
| Create | ✔ | ✔ | ✖ | ✖ | ✖ | ✔ |
| Submit | ✔ | ✔ | ✖ | ✖ | ✖ | ✔ |
| Review | ✖ | ✖ | ✔ | ✖ | ✔ | ✔ |
| Approve | ✖ | ✖ | ✖ | ✖ | ✔ | ✔ |

---

# 12. Progress Report Permissions

| Action | PI | Co-I | Reviewer | Secretary | Chair | Admin |
|----------|-----|------|----------|-----------|-------|-------|
| Submit | ✔ | ✔ | ✖ | ✖ | ✖ | ✔ |
| View | Own | Assigned | Assigned | All | All | All |

---

# 13. Adverse Event Permissions

| Action | PI | Co-I | Reviewer | Secretary | Chair | Admin |
|----------|-----|------|----------|-----------|-------|-------|
| Report | ✔ | ✔ | ✖ | ✖ | ✖ | ✔ |
| Review | ✖ | ✖ | ✔ | ✔ | ✔ | ✔ |

---

# 14. Appeal Permissions

| Action | PI | Co-I | Reviewer | Secretary | Chair | Admin |
|----------|-----|------|----------|-----------|-------|-------|
| Submit Appeal | ✔ | ✖ | ✖ | ✖ | ✖ | ✔ |
| Review Appeal | ✖ | ✖ | ✖ | ✔ | ✔ | ✔ |
| Decide Appeal | ✖ | ✖ | ✖ | ✖ | ✔ | ✔ |

---

# 15. Workflow State Rules (ABAC)

## Draft

Allowed:

- Edit Protocol
- Upload Documents

Not Allowed:

- Reviews
- Decisions

---

## Submitted

Allowed:

- Screening

Not Allowed:

- Protocol Editing

---

## Screening

Allowed:

- Administrative Review

Not Allowed:

- Decision Creation

---

## Review

Allowed:

- Reviewer Activities

Not Allowed:

- Protocol Editing

---

## Meeting

Allowed:

- Voting
- Discussion

Not Allowed:

- Protocol Changes

---

## Decision

Allowed:

- Decision Publication

Decision becomes immutable.

---

## Active

Allowed:

- Progress Reports
- Amendments
- Adverse Event Reporting

---

# 16. Conflict of Interest Rules

## BR-001

Reviewer cannot review:

- Own protocol
- Protocol of direct subordinate
- Protocol with declared conflict

## BR-002

Conflict declaration is mandatory before review assignment.

---

# 17. Tenant Isolation Rules

All permissions are restricted to:

```text
resource.tenant_id == user.tenant_id
```

Exception:

- Future National Registry integration

---

# 18. Audit Requirements

The following actions must generate Audit Events:

- Protocol Submission
- Reviewer Assignment
- Review Submission
- Vote Submission
- Decision Publication
- Amendment Approval
- Appeal Decision

Audit logging cannot be disabled.

---