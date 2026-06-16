# IRB Data Model Specification
Version: 0.1

---

# 1. Overview

Энэхүү систем нь IRB workflow-ийн бүх өгөгдлийг хадгална.

---

# 2. Core Entities

## User

- id (UUID)
- name
- email
- password_hash
- institution_id
- status (active, suspended)

---

## Role

- id
- name (PI, Reviewer, Chair, Admin, Co-Investigator)

---

## UserRole

- user_id
- role_id

(M:N relationship)

---

## Protocol

IRB submission үндсэн объект.

- id
- title
- abstract
- status (draft, submitted, review, approved, rejected, closed)
- pi_id
- institution_id
- risk_level (low, medium, high)
- created_at
- updated_at

---

## ProtocolVersion

Version control шаардлагатай.

- id
- protocol_id
- version_number
- change_summary
- created_at

---

## Document

Upload файлууд.

- id
- protocol_id
- type (protocol, consent, questionnaire, budget)
- file_url
- uploaded_by
- version_id

---

## Review

- id
- protocol_id
- reviewer_id
- score (1–5)
- recommendation (approve, minor, major, reject)
- comments
- submitted_at

---

## CommitteeMeeting

- id
- date
- agenda
- quorum_required
- status

---

## Decision

- id
- protocol_id
- meeting_id
- decision_type (approved, conditional, rejected, deferred)
- decision_letter
- expiry_date
- created_at

---

## Amendment

- id
- protocol_id
- description
- status
- version_id

---

## AuditLog

- id
- user_id
- action
- entity_type
- entity_id
- previous_state
- new_state
- timestamp

---

# 3. Relationships

- User → Protocol (PI)
- Protocol → Review (1:N)
- Protocol → Document (1:N)
- Protocol → Decision (1:1)
- Protocol → Amendment (1:N)
- Review → User (Reviewer)

---

# 4. Notes

- бүх entity дээр audit хийгдэнэ
- protocol versioning mandatory
- decision immutable