# Institutional Review Board (IRB) Management System
Version: 0.1
Status: Draft

---

# 1. System Overview

## Purpose

Энэхүү систем нь судалгааны ёс зүйн хорооны өргөдөл, үнэлгээ, шийдвэр,
баримтжуулалт болон хяналтын үйл ажиллагааг цахимаар удирдана.

## Objectives

- Ethics protocol submission
- Reviewer assignment
- Committee review workflow
- Meeting and agenda management
- Decision recording
- Amendment and continuing review
- Audit and compliance reporting
- Document archive

---

# 2. User Roles

## Principal Investigator (PI)

Судалгааны протокол илгээх.

Permissions:
- Create submission
- Upload documents
- Respond to comments
- View decision
- Submit amendment

---

## Co-Investigator

PI-ийн багт оролцоно.

Permissions:
- View assigned protocol
- Upload supporting files

---

## IRB Reviewer

Хянан үнэлгээ хийх.

Permissions:
- View assigned protocols
- Submit review
- Declare conflict of interest

---

## IRB Chair

Ёс зүйн хурлыг удирдах.

Permissions:
- Assign reviewer
- Finalize recommendation
- Approve meeting agenda

---

## IRB Administrator

Системийн өдөр тутмын үйл ажиллагааг удирдах.

Permissions:
- Manage users
- Configure workflow
- Schedule meetings
- Generate reports

---

# 3. Review Lifecycle

1. Draft submission
2. Submission completed
3. Administrative screening
4. Reviewer assignment
5. Individual review
6. Committee meeting
7. Decision issued
8. Research monitoring
9. Amendment / renewal
10. Closure / archive

---

# 4. Submission Types

## Initial Review
Шинэ судалгааны ёс зүйн зөвшөөрөл.

## Expedited Review
Хялбаршуулсан үнэлгээ.

## Full Board Review
Хорооны бүрэн хэлэлцүүлэг.

## Amendment
Өмнөх зөвшөөрөлд өөрчлөлт.

## Continuing Review
Тогтмол дахин үнэлгээ.

## Adverse Event Report
Сөрөг үйл явдлын мэдээлэл.

## Final Report
Судалгаа хаах тайлан.

---

# 5. Functional Requirements

## FR-001 User Authentication

Users securely authenticate.

Acceptance:
- Email/password
- MFA optional
- Password reset

---

## FR-002 Protocol Submission

PI protocol илгээнэ.

Fields:
- Study title
- Investigators
- Institution
- Funding
- Risk level
- Participant type

Attachments:
- Protocol
- Consent form
- Questionnaire
- Budget
- Approval letters

---

## FR-003 Administrative Screening

Admin completeness шалгана.

Actions:
- Accept screening
- Return for revision
- Request missing files

---

## FR-004 Reviewer Assignment

Chair reviewer томилно.

Acceptance:
- One or more reviewer
- Conflict checking
- Assignment log

---

## FR-005 Reviewer Evaluation

Reviewer ethics evaluation submit хийнэ.

Review form:
- Scientific validity
- Risk-benefit
- Privacy/confidentiality
- Vulnerable population
- Informed consent

Recommendation:
- Approve
- Minor revision
- Major revision
- Reject

---

## FR-006 Committee Meeting

IRB meeting зохион байгуулна.

Features:
- Agenda
- Attendance
- Minutes
- Voting

---

## FR-007 Decision Management

Committee final decision бүртгэнэ.

Decision types:
- Approved
- Conditional approval
- Revision required
- Rejected

Outputs:
- Decision letter
- Notification

---

## FR-008 Amendment Review

PI amendment submit хийнэ.

Requirements:
- Link to prior approval
- Version history
- Review workflow

---

## FR-009 Continuing Review

Approval expiry хянах.

System:
- Reminder
- Renewal workflow
- Expiry warning

---

## FR-010 Audit Log

Critical activity log.

Log:
- User
- Timestamp
- Action
- Previous value
- New value

---

# 6. Business Rules

BR-001
Conflict of interest declared reviewer review хийхгүй.

BR-002
Incomplete submission reviewer stage руу орохгүй.

BR-003
Approval expiry өнгөрвөл study status suspended.

BR-004
Decision нь committee quorum хангагдсан үед хүчинтэй.

BR-005
All decisions immutable audit record-тэй байна.

---

# 7. Data Model

Entities:

- User
- Role
- Institution
- Protocol
- Submission
- Document
- Review
- Meeting
- Agenda
- Vote
- Decision
- Amendment
- AuditLog
- Notification

Relationships:

Protocol
→ many Documents
→ many Reviews
→ one Decision
→ many Amendments

---

# 8. Security & Compliance

Requirements:

- Role-based access control
- Encrypted file storage
- Audit logging
- Secure backup
- Retention policy
- Access history

Sensitive Data:

- Participant information
- Health information
- Investigator documents

---

# 9. Reporting

Reports:

- Submission volume
- Approval rate
- Review turnaround time
- Reviewer workload
- Expiring approvals

---

# 10. Open Questions

- Anonymous reviewer model?
- e-Signature required?
- National ethics registry integration?
- Multi-institution review support?