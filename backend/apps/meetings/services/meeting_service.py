from django.utils import timezone

from apps.meetings.models import Meeting, MeetingStatus

from common.events.publisher import publisher
from common.events.meeting import (
    MeetingCompleted,
    MeetingCancelled,
)

class MeetingService:

    @staticmethod
    def start_meeting(meeting: Meeting):
        if meeting.status != MeetingStatus.SCHEDULED:
            raise ValueError("Meeting can only be started from scheduled status.")

        meeting.status = MeetingStatus.IN_PROGRESS
        meeting.save(update_fields=["status", "updated_at"])

        return meeting

    @staticmethod
    def complete_meeting(meeting: Meeting):
        if meeting.status != MeetingStatus.IN_PROGRESS:
            raise ValueError("Meeting is not in progress.")

        meeting.status = MeetingStatus.COMPLETED
        meeting.save(update_fields=["status", "updated_at"])

        publisher.publish(
            MeetingCompleted(
                tenant_id=meeting.tenant_id,
                actor_id=None,
                meeting_id=meeting.id,
                protocol_id=meeting.protocol_id,
            )
        )

        return meeting

    @staticmethod
    def cancel_meeting(meeting: Meeting):
        if meeting.status == MeetingStatus.COMPLETED:
            raise ValueError("Completed meeting cannot be cancelled.")

        meeting.status = MeetingStatus.CANCELLED
        meeting.save(update_fields=["status", "updated_at"])

        publisher.publish(
            MeetingCancelled(
                tenant_id=meeting.tenant_id,
                actor_id=None,
                meeting_id=meeting.id,
                protocol_id=meeting.protocol_id,
            )
        )

        return meeting
