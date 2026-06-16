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

# Appendix A – Permission Catalog

This appendix defines system-level permission codes used by the authorization engine.

Permission codes are machine-readable identifiers used by:

- Backend authorization middleware
- API access control
- Workflow enforcement
- Audit logging
- Role assignment

---

## A.1 Protocol Permissions

```text
protocol.create
protocol.view
protocol.edit
protocol.submit
protocol.withdraw
protocol.archive
```

---

## A.2 Protocol Version Permissions

```text
protocol_version.create
protocol_version.view
protocol_version.compare
```

---

## A.3 Document Permissions

```text
document.upload
document.view
document.download
document.delete
```

---

## A.4 Review Assignment Permissions

```text
review_assignment.create
review_assignment.view
review_assignment.update
review_assignment.cancel
```

---

## A.5 Review Permissions

```text
review.create
review.view
review.edit
review.submit
review.reopen
```

---

## A.6 Meeting Permissions

```text
meeting.create
meeting.view
meeting.edit
meeting.close
```

---

## A.7 Agenda Permissions

```text
agenda.create
agenda.view
agenda.edit
agenda.remove
```

---

## A.8 Vote Permissions

```text
vote.create
vote.view
vote.finalize
```

---

## A.9 Decision Permissions

```text
decision.create
decision.view
decision.approve
decision.publish
decision.revoke
```

---

## A.10 Amendment Permissions

```text
amendment.create
amendment.submit
amendment.review
amendment.approve
```

---

## A.11 Progress Report Permissions

```text
progress_report.create
progress_report.submit
progress_report.view
```

---

## A.12 Adverse Event Permissions

```text
adverse_event.create
adverse_event.submit
adverse_event.review
```

---

## A.13 Appeal Permissions

```text
appeal.create
appeal.submit
appeal.review
appeal.decide
```

---

## A.14 Committee Permissions

```text
committee.create
committee.view
committee.edit
committee.manage_members
```

---

## A.15 User Administration Permissions

```text
user.create
user.view
user.edit
user.disable
```

---

## A.16 Role Administration Permissions

```text
role.assign
role.revoke
```

---

## A.17 Audit Permissions

```text
audit.view
audit.export
```

---

# Appendix B – Authorization Evaluation Order

All authorization decisions must follow the sequence below:

```text
Authentication
        ↓
Tenant Validation
        ↓
RBAC Permission Check
        ↓
Workflow State Validation
        ↓
Ownership Validation
        ↓
Conflict of Interest Validation
        ↓
Authorization Result
```

---

# Appendix C – Role Mapping

## Admin

All permissions within tenant scope.

---

## Chair

Committee management, reviewer oversight, voting authority, and decision approval.

Typical permissions:

```text
review_assignment.create
meeting.create
vote.finalize
decision.create
decision.approve
decision.publish
```

---

## Secretary

Workflow coordination and committee administration.

Typical permissions:

```text
review_assignment.create
meeting.create
meeting.edit
agenda.create
agenda.edit
```

---

## Reviewer

Assigned review activities and voting rights.

Typical permissions:

```text
review.view
review.create
review.edit
review.submit
vote.create
```

---

## PI (Principal Investigator)

Protocol ownership and lifecycle management.

Typical permissions:

```text
protocol.create
protocol.edit
protocol.submit
amendment.create
progress_report.submit
appeal.submit
```

---

## Co-Investigator

Protocol collaboration and supporting submissions.

Typical permissions:

```text
protocol.view
document.upload
amendment.create
progress_report.create
```

---

# Version History

| Version | Description |
|----------|-------------|
| 0.1 | Initial RBAC model |
| 0.2 | Workflow and committee integration |
| 1.0 | Permission Catalog and ABAC integration |

---