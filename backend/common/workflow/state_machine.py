from enum import StrEnum


class ProtocolStatus(StrEnum):
    DRAFT = "draft"

    SUBMITTED = "submitted"

    PRE_SCREENING = "pre_screening"

    UNDER_REVIEW = "under_review"

    COMMITTEE_REVIEW = "committee_review"

    REVISION_REQUIRED = "revision_required"

    APPROVED = "approved"

    REJECTED = "rejected"

    WITHDRAWN = "withdrawn"

    ALLOWED_TRANSITIONS = {

        ProtocolStatus.DRAFT: {
            ProtocolStatus.SUBMITTED,
        },

        ProtocolStatus.SUBMITTED: {
            ProtocolStatus.PRE_SCREENING,
            ProtocolStatus.WITHDRAWN,
        },

        ProtocolStatus.PRE_SCREENING: {
            ProtocolStatus.UNDER_REVIEW,
            ProtocolStatus.REVISION_REQUIRED,
            ProtocolStatus.REJECTED,
        },

        ProtocolStatus.UNDER_REVIEW: {
            ProtocolStatus.COMMITTEE_REVIEW,
            ProtocolStatus.REVISION_REQUIRED,
            ProtocolStatus.REJECTED,
        },

        ProtocolStatus.COMMITTEE_REVIEW: {
            ProtocolStatus.APPROVED,
            ProtocolStatus.REJECTED,
            ProtocolStatus.REVISION_REQUIRED,
        },

        ProtocolStatus.REVISION_REQUIRED: {
            ProtocolStatus.SUBMITTED,
            ProtocolStatus.WITHDRAWN,
        },

        ProtocolStatus.APPROVED: set(),

        ProtocolStatus.REJECTED: set(),

        ProtocolStatus.WITHDRAWN: set(),
    }