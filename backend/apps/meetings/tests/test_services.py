from django.test import TestCase
from django.utils import timezone

from apps.meetings.models import (
    Meeting,
    MeetingAgenda,
    MeetingParticipant,
    MeetingVote,
    MeetingStatus,
    ParticipantRole,
    AttendanceStatus,
    VoteChoice,
)

from apps.meetings.services import (
    AgendaService,
    MeetingService,
    ParticipantService,
    QuorumService,
    VotingService,
)

from apps.protocols.models import (
    Protocol,
    RiskLevel,
)

from apps.tenants.models import Tenant
from apps.users.models import User


class MeetingServiceTest(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="must",
            name="MUST",
        )

        self.chair = User.objects.create_user(
            email="chair@example.com",
            password="password123",
        )

        self.meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="IRB Committee Meeting",
            meeting_date=timezone.now(),
            chair=self.chair,
        )

    def test_start_meeting(self):
        MeetingService.start_meeting(self.meeting)

        self.meeting.refresh_from_db()

        self.assertEqual(
            self.meeting.status,
            MeetingStatus.IN_PROGRESS,
        )

    def test_complete_meeting(self):
        MeetingService.start_meeting(self.meeting)
        MeetingService.complete_meeting(self.meeting)

        self.meeting.refresh_from_db()

        self.assertEqual(
            self.meeting.status,
            MeetingStatus.COMPLETED,
        )

    def test_cancel_meeting(self):
        MeetingService.cancel_meeting(self.meeting)

        self.meeting.refresh_from_db()

        self.assertEqual(
            self.meeting.status,
            MeetingStatus.CANCELLED,
        )

class ParticipantServiceTest(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="must",
            name="MUST",
        )

        self.chair = User.objects.create_user(
            email="chair@example.com",
            password="password123",
        )

        self.reviewer = User.objects.create_user(
            email="reviewer@example.com",
            password="password123",
        )

        self.meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="IRB Committee Meeting",
            meeting_date=timezone.now(),
            chair=self.chair,
        )

    def test_add_participant(self):
        participant = ParticipantService.add_participant(
            meeting=self.meeting,
            user=self.reviewer,
        )

        self.assertEqual(
            participant.user,
            self.reviewer,
        )

        self.assertEqual(
            participant.role,
            ParticipantRole.REVIEWER,
        )

    def test_mark_attendance(self):
        participant = ParticipantService.add_participant(
            meeting=self.meeting,
            user=self.reviewer,
        )

        ParticipantService.mark_attendance(
            participant,
            AttendanceStatus.PRESENT,
        )

        participant.refresh_from_db()

        self.assertEqual(
            participant.attendance_status,
            AttendanceStatus.PRESENT,
        )

    def test_remove_participant(self):
        participant = ParticipantService.add_participant(
            meeting=self.meeting,
            user=self.reviewer,
        )

        ParticipantService.remove_participant(participant)

        self.assertFalse(
            MeetingParticipant.objects.filter(
                id=participant.id,
            ).exists()
        )

class AgendaServiceTest(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="must",
            name="MUST",
        )

        self.chair = User.objects.create_user(
            email="chair@example.com",
            password="password123",
        )

        self.meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="IRB Committee Meeting",
            meeting_date=timezone.now(),
            chair=self.chair,
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Cancer Study",
            protocol_number="IRB-001",
            principal_investigator=self.chair,
            risk_level=RiskLevel.LOW,
        )

    def test_add_protocol(self):
        agenda = AgendaService.add_protocol(
            meeting=self.meeting,
            protocol=self.protocol,
            order=1,
            presenter=self.chair,
        )

        self.assertEqual(agenda.meeting, self.meeting)
        self.assertEqual(agenda.protocol, self.protocol)
        self.assertEqual(agenda.order, 1)

    def test_reorder_agenda(self):
        agenda = AgendaService.add_protocol(
            meeting=self.meeting,
            protocol=self.protocol,
            order=1,
        )

        AgendaService.reorder_agenda(
            agenda=agenda,
            new_order=2,
        )

        agenda.refresh_from_db()

        self.assertEqual(agenda.order, 2)

    def test_remove_agenda_item(self):
        agenda = AgendaService.add_protocol(
            meeting=self.meeting,
            protocol=self.protocol,
            order=1,
        )

        agenda_id = agenda.id

        AgendaService.remove_agenda_item(agenda)

        self.assertFalse(
            MeetingAgenda.objects.filter(
                id=agenda_id,
            ).exists()
        )

class VotingServiceTest(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="must",
            name="MUST",
        )

        self.chair = User.objects.create_user(
            email="chair@example.com",
            password="password123",
        )

        self.reviewer = User.objects.create_user(
            email="reviewer@example.com",
            password="password123",
        )

        self.meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="IRB Meeting",
            meeting_date=timezone.now(),
            chair=self.chair,
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Cancer Study",
            protocol_number="IRB-001",
            principal_investigator=self.chair,
            risk_level=RiskLevel.LOW,
        )

        self.participant = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.reviewer,
            role=ParticipantRole.REVIEWER,
        )

        self.agenda = MeetingAgenda.objects.create(
            meeting=self.meeting,
            protocol=self.protocol,
            order=1,
            presenter=self.chair,
        )

    def test_cast_vote(self):
        vote = VotingService.cast_vote(
            agenda=self.agenda,
            participant=self.participant,
            vote=VoteChoice.APPROVE,
            comment="Approved",
        )

        self.assertEqual(vote.vote, VoteChoice.APPROVE)
        self.assertEqual(vote.participant, self.participant)

    def test_update_vote(self):
        vote = VotingService.cast_vote(
            agenda=self.agenda,
            participant=self.participant,
            vote=VoteChoice.APPROVE,
        )

        VotingService.update_vote(
            meeting_vote=vote,
            vote=VoteChoice.REJECT,
            comment="Need revisions",
        )

        vote.refresh_from_db()

        self.assertEqual(vote.vote, VoteChoice.REJECT)
        self.assertEqual(vote.comment, "Need revisions")

    def test_count_votes(self):
        VotingService.cast_vote(
            agenda=self.agenda,
            participant=self.participant,
            vote=VoteChoice.APPROVE,
        )

        results = VotingService.count_votes(
            self.agenda,
        )

        self.assertEqual(
            results[VoteChoice.APPROVE],
            1,
        )

        self.assertEqual(
            results[VoteChoice.REJECT],
            0,
        )

class QuorumServiceTest(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="must",
            name="MUST",
        )

        self.chair = User.objects.create_user(
            email="chair@example.com",
            password="password123",
        )

        self.reviewer1 = User.objects.create_user(
            email="reviewer1@example.com",
            password="password123",
        )

        self.reviewer2 = User.objects.create_user(
            email="reviewer2@example.com",
            password="password123",
        )

        self.reviewer3 = User.objects.create_user(
            email="reviewer3@example.com",
            password="password123",
        )

        self.reviewer4 = User.objects.create_user(
            email="reviewer4@example.com",
            password="password123",
        )

        self.meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="IRB Committee Meeting",
            meeting_date=timezone.now(),
            chair=self.chair,
        )

        self.participant1 = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.reviewer1,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.PRESENT,
        )

        self.participant2 = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.reviewer2,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.PRESENT,
        )

        self.participant3 = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.reviewer3,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.ABSENT,
        )

        self.participant4 = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.reviewer4,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.ABSENT,
        )

    def test_present_participants(self):
        participants = QuorumService.present_participants(
            self.meeting,
        )

        self.assertEqual(
            participants.count(),
            2,
        )

    def test_present_count(self):
        self.assertEqual(
            QuorumService.present_count(
                self.meeting,
            ),
            2,
        )

    def test_total_participants(self):
        self.assertEqual(
            QuorumService.total_participants(
                self.meeting,
            ),
            4,
        )

    def test_has_quorum(self):
        self.assertTrue(
            QuorumService.has_quorum(
                self.meeting,
            )
        )

    def test_attendance_percentage(self):
        self.assertEqual(
            QuorumService.attendance_percentage(
                self.meeting,
            ),
            50.0,
        )
