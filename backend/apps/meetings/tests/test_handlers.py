from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.meetings.handlers import MeetingHandler


class MeetingHandlerTest(SimpleTestCase):

    @patch(
        "apps.meetings.handlers.CommitteeDecisionService.create_from_agenda"
    )
    @patch("apps.meetings.handlers.Meeting")
    def test_handle_meeting_completed(
        self,
        meeting_model,
        create_from_agenda,
    ):
        meeting = MagicMock()

        agenda1 = MagicMock()
        agenda2 = MagicMock()

        meeting.agenda_items.all.return_value = [
            agenda1,
            agenda2,
        ]

        meeting_model.objects.prefetch_related.return_value.get.return_value = (
            meeting
        )

        event = MagicMock()
        event.payload = {
            "meeting_id": "meeting-id",
        }

        MeetingHandler.handle_meeting_completed(event)

        self.assertEqual(
            create_from_agenda.call_count,
            2,
        )

        create_from_agenda.assert_any_call(agenda1)
        create_from_agenda.assert_any_call(agenda2)
