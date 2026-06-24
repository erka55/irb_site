from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class ReviewSubmitted:
    review_id: UUID
    protocol_id: UUID
    reviewer_id: UUID
    submitted_at: datetime
