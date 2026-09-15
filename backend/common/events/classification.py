from common.events.base import BaseEvent
from common.events.types import EventTypes


class ClassificationAssessed(BaseEvent):

    def __init__(
        self,
        *,
        assessment_id,
        protocol_id,
        protocol_version_id,
        classification,
        **kwargs,
    ):
        super().__init__(
            event_type=EventTypes.CLASSIFICATION_ASSESSED,
            **kwargs,
        )

        self.payload.update(
            {
                "assessment_id": str(assessment_id),
                "protocol_id": str(protocol_id),
                "protocol_version_id": str(protocol_version_id),
                "classification": classification,
            }
        )
