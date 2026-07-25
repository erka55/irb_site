from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ReviewCompleted:
    protocol_id: UUID
    review_id: UUID
    reviewer_id: UUID

@dataclass(frozen=True)
class ReviewsCompleted:
    protocol_id: UUID
