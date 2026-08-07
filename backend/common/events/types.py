class EventTypes:
    # Protocol Events
    PROTOCOL_SUBMITTED = "protocol.submitted"
    PROTOCOL_UPDATED = "protocol.updated"
    PROTOCOL_APPROVED = "protocol.approved"
    PROTOCOL_REJECTED = "protocol.rejected"
    PROTOCOL_REVISIONS_REQUESTED = "protocol.revisions_requested"

    # Review Events
    REVIEW_ASSIGNED = "review.assigned"
    REVIEW_SUBMITTED = "review.submitted"
    REVIEW_COMPLETED = "review.completed"
    REVIEWS_COMPLETED = "reviews.completed"

    # Meeting Events
    MEETING_SCHEDULED = "meeting.scheduled"
    MEETING_COMPLETED = "meeting.completed"
    MEETING_CANCELLED = "meeting.cancelled"

    # Decision Events
    DECISION_CREATED = "decision.created"
    DECISION_LETTER_GENERATED = "decision.letter.generated"
    DECISION_ISSUED = "decision.issued"
    DECISION_PUBLISHED = "decision.published"
    DECISION_LETTER_ISSUED = "decision.letter.issued"