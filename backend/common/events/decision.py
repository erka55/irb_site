from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class DecisionCreated:
    protocol_id: UUID
    decision_id: UUID
