from unittest.mock import MagicMock

from django.test import SimpleTestCase

from apps.decision.models import Decision
from apps.decision.services import CommitteeDecisionService
from apps.meetings.models import MeetingStatus, VoteChoice


class CommitteeDecisionServiceTest(SimpleTestCase):

    def _agenda(self, meeting_status=MeetingStatus.COMPLETED):
        meeting = MagicMock()
        meeting.status = meeting_status

        agenda = MagicMock()
        agenda.meeting = meeting
        agenda.protocol = MagicMock()

        agenda.votes = MagicMock()

        return agenda

    def test_validate_requires_completed_meeting(self):
        agenda = self._agenda(MeetingStatus.SCHEDULED)

        with self.assertRaises(ValueError):
            CommitteeDecisionService.validate_agenda(agenda)

    def test_determine_decision_type_approved(self):
        agenda = self._agenda()

        agenda.votes.exists.return_value = True
        agenda.votes.all.return_value = [
            MagicMock(vote=VoteChoice.APPROVE),
            MagicMock(vote=VoteChoice.APPROVE),
            MagicMock(vote=VoteChoice.REJECT),
        ]

        result = CommitteeDecisionService.determine_decision_type(
            agenda
        )

        self.assertEqual(
            result,
            Decision.DecisionType.APPROVED,
        )

    def test_determine_decision_type_rejected(self):
        agenda = self._agenda()

        agenda.votes.exists.return_value = True
        agenda.votes.all.return_value = [
            MagicMock(vote=VoteChoice.REJECT),
            MagicMock(vote=VoteChoice.REJECT),
            MagicMock(vote=VoteChoice.APPROVE),
        ]

        result = CommitteeDecisionService.determine_decision_type(
            agenda
        )

        self.assertEqual(
            result,
            Decision.DecisionType.REJECTED,
        )

    def test_determine_decision_type_abstain_only(self):
        agenda = self._agenda()

        agenda.votes.exists.return_value = True
        agenda.votes.all.return_value = [
            MagicMock(vote=VoteChoice.ABSTAIN),
            MagicMock(vote=VoteChoice.ABSTAIN),
        ]

        with self.assertRaises(ValueError):
            CommitteeDecisionService.determine_decision_type(
                agenda
            )
