from common.events.base import BaseEvent


class MeetingHandler:
    """
    Handles meeting-related domain events.
    """

    @staticmethod
    def handle_meeting_completed(event: BaseEvent):
        """
        Handle meeting completed event.
        """
        pass

    @staticmethod
    def handle_meeting_cancelled(event: BaseEvent):
        """
        Handle meeting cancelled event.
        """
        pass
