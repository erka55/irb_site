from django.test import TestCase
from django.utils import timezone

from apps.meetings.models import (
    Meeting,
    MeetingAgenda,
    MeetingParticipant,
    MeetingStatus,
    ParticipantRole,
    AttendanceStatus,
)

from apps.meetings.services import (
    AgendaService,
    MeetingService,
    ParticipantService,
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
