from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class ReviewAssigned:
    review_id: UUID
    protocol_id: UUID
    reviewer_id: UUID
    assigned_at: datetime
