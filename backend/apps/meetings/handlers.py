from common.events.base import BaseEvent

from apps.meetings.models import Meeting
from apps.decision.services import CommitteeDecisionService


class MeetingHandler:
    """
    Handles meeting-related domain events.
    """

    @staticmethod
    def handle_meeting_completed(event: BaseEvent):
        """
        Create draft decisions for all agenda items
        after a meeting has been completed.
        """

        meeting = Meeting.objects.prefetch_related(
            "agenda_items"
        ).get(
            id=event.payload["meeting_id"]
        )

        for agenda in meeting.agenda_items.all():
            CommitteeDecisionService.create_from_agenda(
                agenda
            )

    @staticmethod
    def handle_meeting_cancelled(event: BaseEvent):
        """
        Handle meeting cancelled event.
        """
        return
