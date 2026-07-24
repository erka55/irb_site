from enum import StrEnum


class ProtocolStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISIONS_REQUIRED = "revisions_required"


ALLOWED_TRANSITIONS = {
    ProtocolStatus.DRAFT: {
        ProtocolStatus.SUBMITTED,
    },

    ProtocolStatus.SUBMITTED: {
        ProtocolStatus.UNDER_REVIEW,
    },

    ProtocolStatus.UNDER_REVIEW: {
        ProtocolStatus.APPROVED,
        ProtocolStatus.REJECTED,
        ProtocolStatus.REVISIONS_REQUIRED,
    },

    ProtocolStatus.REVISIONS_REQUIRED: {
        ProtocolStatus.SUBMITTED,
    },

    ProtocolStatus.APPROVED: set(),

    ProtocolStatus.REJECTED: set(),
}
