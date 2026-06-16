# IRB Database Schema Specification
Version: 0.1

Database:
PostgreSQL 16+

Naming Convention:
snake_case

Primary Keys:
UUID

Timestamp:
UTC

Soft Delete:
deleted_at nullable

--------------------------------------------------
1. USERS
--------------------------------------------------

Table: users

id                  UUID PK
email               VARCHAR(255) UNIQUE NOT NULL
password_hash       TEXT NOT NULL

first_name          VARCHAR(100)
last_name           VARCHAR(100)

phone               VARCHAR(50)

is_active           BOOLEAN DEFAULT TRUE

created_at          TIMESTAMP
updated_at          TIMESTAMP
deleted_at          TIMESTAMP NULL

Indexes:

idx_users_email

--------------------------------------------------
2. ROLES
--------------------------------------------------

Table: roles

id                  UUID PK
name                VARCHAR(50) UNIQUE

Examples:

PI
REVIEWER
CHAIR
ADMIN

--------------------------------------------------
3. USER ROLES
--------------------------------------------------

Table: user_roles

user_id             UUID FK users
role_id             UUID FK roles

PRIMARY KEY
(user_id, role_id)

--------------------------------------------------
4. INSTITUTIONS
--------------------------------------------------

Table: institutions

id                  UUID PK

name                VARCHAR(255)

country             VARCHAR(100)

created_at
updated_at

--------------------------------------------------
5. PROTOCOLS
--------------------------------------------------

Table: protocols

id                  UUID PK

protocol_number     VARCHAR(50) UNIQUE

title               TEXT

abstract            TEXT

status              VARCHAR(50)

risk_level          VARCHAR(50)

pi_id               UUID FK users

institution_id      UUID FK institutions

current_version     INTEGER

submitted_at        TIMESTAMP NULL

created_at
updated_at

Status Values:

draft
submitted
screening
review
approved
rejected
closed

Indexes:

idx_protocol_status
idx_protocol_pi
idx_protocol_institution

--------------------------------------------------
6. PROTOCOL VERSIONS
--------------------------------------------------

Table: protocol_versions

id                  UUID PK

protocol_id         UUID FK protocols

version_number      INTEGER

change_summary      TEXT

created_by          UUID FK users

created_at

UNIQUE

(protocol_id, version_number)

--------------------------------------------------
7. DOCUMENTS
--------------------------------------------------

Table: documents

id                  UUID PK

protocol_id         UUID FK protocols

version_id          UUID FK protocol_versions

document_type       VARCHAR(50)

file_name           TEXT

file_path           TEXT

mime_type           VARCHAR(100)

file_size           BIGINT

uploaded_by         UUID FK users

created_at

Document Types:

protocol
consent_form
questionnaire
budget
cv
approval_letter
other

--------------------------------------------------
8. REVIEW ASSIGNMENTS
--------------------------------------------------

Table: review_assignments

id                  UUID PK

protocol_id         UUID FK protocols

reviewer_id         UUID FK users

assigned_by         UUID FK users

due_date            DATE

status              VARCHAR(50)

assigned_at         TIMESTAMP

Status:

assigned
completed
declined

Indexes:

idx_assignment_reviewer

--------------------------------------------------
9. REVIEWS
--------------------------------------------------

Table: reviews

id                  UUID PK

protocol_id         UUID FK protocols

reviewer_id         UUID FK users

scientific_score    INTEGER

risk_score          INTEGER

privacy_score       INTEGER

consent_score       INTEGER

recommendation      VARCHAR(50)

comments            TEXT

submitted_at        TIMESTAMP

Recommendation:

approve
minor_revision
major_revision
reject

Indexes:

idx_review_protocol

--------------------------------------------------
10. COMMITTEE MEETINGS
--------------------------------------------------

Table: committee_meetings

id                  UUID PK

meeting_date        DATE

title               TEXT

agenda              TEXT

quorum_required     INTEGER

status              VARCHAR(50)

created_at

--------------------------------------------------
11. MEETING ATTENDEES
--------------------------------------------------

Table: meeting_attendees

meeting_id          UUID FK committee_meetings

user_id             UUID FK users

attendance_status   VARCHAR(50)

PRIMARY KEY

(meeting_id,user_id)

--------------------------------------------------
12. DECISIONS
--------------------------------------------------

Table: decisions

id                  UUID PK

protocol_id         UUID FK protocols

meeting_id          UUID FK committee_meetings

decision_type       VARCHAR(50)

decision_letter     TEXT

expiry_date         DATE

issued_by           UUID FK users

issued_at           TIMESTAMP

Decision Types:

approved
conditional
rejected
deferred

Indexes:

idx_decision_protocol

--------------------------------------------------
13. NOTIFICATIONS
--------------------------------------------------

Table: notifications

id                  UUID PK

user_id             UUID FK users

title               TEXT

message             TEXT

is_read             BOOLEAN

created_at

--------------------------------------------------
14. AUDIT LOGS
--------------------------------------------------

Table: audit_logs

id                  UUID PK

user_id             UUID FK users

action              VARCHAR(100)

entity_type         VARCHAR(100)

entity_id           UUID

old_value           JSONB

new_value           JSONB

ip_address          VARCHAR(100)

created_at          TIMESTAMP

Indexes:

idx_audit_entity

idx_audit_user

idx_audit_created

--------------------------------------------------
15. WORKFLOW HISTORY
--------------------------------------------------

Table: workflow_history

id                  UUID PK

protocol_id         UUID FK protocols

from_state          VARCHAR(50)

to_state            VARCHAR(50)

transition_by       UUID FK users

comment             TEXT

created_at

--------------------------------------------------
16. EMAIL QUEUE
--------------------------------------------------

Table: email_queue

id                  UUID PK

recipient           VARCHAR(255)

subject             TEXT

body                TEXT

status              VARCHAR(50)

retry_count         INTEGER

created_at

Status:

pending
sent
failed