# IRB Workflow Specification

Version: 1.0
Status: Freeze

---

# 1. Purpose

This document defines the lifecycle of research protocols within the IRB System.

Workflow is the authoritative source of state transitions.

No protocol state may change outside the workflow engine.

---

# 2. Core Workflow

```text
Draft
  ↓
Submitted
  ↓
Screening
  ↓
Review
  ↓
Meeting
  ↓
Decision
  ↓
Active
  ↓
Closed
```

---

# 3. Workflow States

## 3.1 Draft

Protocol is being prepared by the PI.

Allowed Actions:

- Edit Protocol
- Upload Documents
- Add Co-Investigators
- Delete Draft

Allowed Roles:

- PI
- Co-Investigator

Transition Events:

```text
submit_protocol
```

Next State:

```text
Submitted
```

---

## 3.2 Submitted

Protocol has been formally submitted.

Allowed Actions:

- View Submission

Allowed Roles:

- PI
- Secretary
- Chair

Transition Events:

```text
start_screening
withdraw_protocol
```

Possible Next States:

```text
Screening
Withdrawn
```

---

## 3.3 Screening

Administrative completeness review.

Performed By:

- Secretary

Validation Rules:

- Required documents present
- Required fields completed
- Submission category assigned

Transition Events:

```text
screening_passed
screening_failed
```

Possible Next States:

```text
Review
Draft
```

---

## 3.4 Review

Scientific and ethical review.

Performed By:

- Assigned Reviewers

Allowed Actions:

- Submit Review
- Update Review

Business Rules:

- Conflict of interest check
- Reviewer assignment required

Transition Events:

```text
all_reviews_received
request_revision
```

Possible Next States:

```text
Meeting
Draft
```

---

## 3.5 Meeting

Committee discussion and voting.

Performed By:

- Chair
- Committee Members

Requirements:

- Quorum achieved
- Agenda finalized

Allowed Actions:

- Vote
- Record Discussion

Transition Events:

```text
meeting_completed
meeting_deferred
```

Possible Next States:

```text
Decision
Review
```

---

## 3.6 Decision

Official decision issued.

Performed By:

- Chair

Decision Types:

- Approved
- Conditional Approval
- Additional Information Required
- Rejected

Transition Events:

```text
approve_protocol
conditional_approval
request_information
reject_protocol
```

Possible Next States:

```text
Active
Draft
Rejected
```

---

## 3.7 Active

Approved protocol is active.

Allowed Activities:

- Progress Reports
- Amendments
- Adverse Event Reporting

Transition Events:

```text
close_protocol
suspend_protocol
```

Possible Next States:

```text
Closed
Suspended
```

---

## 3.8 Suspended

Protocol temporarily halted.

Performed By:

- Chair
- IRB

Transition Events:

```text
reinstate_protocol
terminate_protocol
```

Possible Next States:

```text
Active
Closed
```

---

## 3.9 Closed

Protocol completed.

Characteristics:

- Read-only
- No further amendments allowed

Terminal State:

```text
Closed
```

---

## 3.10 Withdrawn

Protocol withdrawn by PI before review completion.

Characteristics:

- Read-only
- Audit preserved

Terminal State:

```text
Withdrawn
```

---

## 3.11 Rejected

Protocol rejected by IRB.

Characteristics:

- No activation permitted
- Appeal allowed

Terminal State:

```text
Rejected
```

---

# 4. Workflow Events

## Submission Events

```text
submit_protocol
withdraw_protocol
```

---

## Screening Events

```text
start_screening
screening_passed
screening_failed
```

---

## Review Events

```text
assign_reviewer
submit_review
all_reviews_received
request_revision
```

---

## Meeting Events

```text
schedule_meeting
meeting_completed
meeting_deferred
```

---

## Decision Events

```text
approve_protocol
conditional_approval
request_information
reject_protocol
```

---

## Monitoring Events

```text
submit_progress_report
submit_amendment
report_adverse_event
```

---

## Closure Events

```text
close_protocol
suspend_protocol
reinstate_protocol
terminate_protocol
```

---

# 5. Workflow Rules

## BR-001

Protocol cannot enter Review without:

- Screening completed

---

## BR-002

Protocol cannot enter Meeting without:

- At least one completed review

---

## BR-003

Meeting cannot complete without quorum.

---

## BR-004

Decision cannot be issued without recorded meeting outcome.

---

## BR-005

Active protocol may submit amendments at any time.

---

## BR-006

Closed protocol cannot be modified.

---

## BR-007

Decision records are immutable after publication.

---

# 6. Workflow and RBAC Integration

Example:

```text
review.submit
```

Permission alone is insufficient.

Additional checks:

```text
workflow_state == Review
AND
reviewer_assigned == true
AND
conflict_of_interest == false
```

must all be satisfied.

---

# 7. Workflow Audit Requirements

Every state transition must create an AuditEvent.

Required Fields:

- actor_id
- protocol_id
- previous_state
- new_state
- event_name
- timestamp

Example:

```json
{
  "event": "screening_passed",
  "from": "Screening",
  "to": "Review"
}
```

---

# 8. State Transition Matrix

| Current State | Event | Next State |
|---------------|--------|------------|
| Draft | submit_protocol | Submitted |
| Submitted | start_screening | Screening |
| Screening | screening_passed | Review |
| Screening | screening_failed | Draft |
| Review | all_reviews_received | Meeting |
| Review | request_revision | Draft |
| Meeting | meeting_completed | Decision |
| Meeting | meeting_deferred | Review |
| Decision | approve_protocol | Active |
| Decision | conditional_approval | Draft |
| Decision | request_information | Draft |
| Decision | reject_protocol | Rejected |
| Active | suspend_protocol | Suspended |
| Active | close_protocol | Closed |
| Suspended | reinstate_protocol | Active |
| Suspended | terminate_protocol | Closed |

---

# 9. Freeze Status

Workflow Version: 1.0

Validated Against:

- architecture.md v0.2
- data-model.md v0.1
- rbac.md v1.0
- database-schema.md v1.0

This workflow is the authoritative state machine for the IRB System.

---