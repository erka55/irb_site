from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import uuid4
from typing import Any


@dataclass(slots=True)
class BaseEvent:
    """
    Base class for all domain events.
    """

    event_type: str
    tenant_id: str
    actor_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)

    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
