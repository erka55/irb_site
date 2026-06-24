from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class ReviewAggregated:
    protocol_id: UUID
    aggregated_at: datetime
    review_count: int
    average_score: float
