# IRB RBAC (Role-Based Access Control)
Version: 0.1

---

# 1. Roles

- PI (Principal Investigator)
- Co-Investigator
- Reviewer
- Chair
- Admin

---

# 2. Permission Model

Format:

ACTION + RESOURCE

---

# 3. Permissions

## Protocol

| Action | PI | Reviewer | Chair | Admin |
|---|---|---|---|---|
| create | ✔ | ✖ | ✖ | ✔ |
| view | own | assigned | all | all |
| edit | own draft | ✖ | ✔ (metadata) | ✔ |
| submit | ✔ | ✖ | ✖ | ✔ |
| withdraw | ✔ | ✖ | ✔ (override) | ✔ |

---

## Review

| Action | PI | Reviewer | Chair | Admin |
|---|---|---|---|---|
| create | ✖ | ✔ | ✔ | ✖ |
| edit | ✖ | own only | ✔ | ✔ |
| submit | ✖ | ✔ | ✔ | ✔ |
| view | own protocol | assigned | all | all |

---

## Decision

| Action | PI | Reviewer | Chair | Admin |
|---|---|---|---|---|
| create | ✖ | ✖ | ✔ | ✔ |
| approve | ✖ | ✖ | ✔ | ✔ |
| view | own | assigned | all | all |

---

## Document

| Action | PI | Reviewer | Chair | Admin |
|---|---|---|---|---|
| upload | ✔ | ✖ | ✖ | ✔ |
| view | own | assigned | all | all |
| delete | own draft | ✖ | ✔ | ✔ |

---

# 4. Special Rules

BR-001
Reviewer өөрийн protocol дээр ажиллах эрхгүй.

BR-002
Admin бүх эрхтэй боловч decision override хийхдээ log үүсгэнэ.

BR-003
Chair final approval эрхтэй.

---

# 5. Scope Rules

- OWN: өөрийн үүсгэсэн
- ASSIGNED: томилогдсон
- ALL: системийн бүх өгөгдөл