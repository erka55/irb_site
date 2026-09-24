from django.test import TestCase
from django.utils import timezone

from django.db import IntegrityError
from apps.meetings.models import (
    Meeting,
    MeetingMinutes,
    MeetingParticipant,
    MeetingAgenda,
    MeetingVote,
    ParticipantRole,
    VoteChoice,
)
from apps.tenants.models import Tenant
from apps.users.models import User

from apps.protocols.models import (
    Protocol,
    RiskLevel,
)


class MeetingModelTest(TestCase):
    def test_create_meeting(self):
        tenant = Tenant.objects.create(
            code="TEST",
            name="Test Tenant",
        )

        chair = User.objects.create_user(
            email="chair@test.com",
            password="password123",
        )

        meeting = Meeting.objects.create(
            tenant=tenant,
            title="IRB Meeting",
            meeting_date="2026-08-15T10:00:00Z",
            chair=chair,
        )

        self.assertEqual(meeting.title, "IRB Meeting")

class MeetingMinutesModelTest(TestCase):

    def test_create_meeting_minutes(self):
        tenant = Tenant.objects.create(
            code="must",
            name="MUST",
        )

        chair = User.objects.create_user(
            email="chair@example.com",
            password="password123",
        )

        meeting = Meeting.objects.create(
            tenant=tenant,
            title="IRB Committee Meeting",
            meeting_date=timezone.now(),
            chair=chair,
        )

        recorded_at = timezone.now()

        minutes = MeetingMinutes.objects.create(
            tenant=tenant,
            meeting=meeting,
            content="Committee reviewed the submitted protocol.",
            recorded_at=recorded_at,
        )

        self.assertEqual(minutes.tenant, tenant)
        self.assertEqual(minutes.meeting, meeting)
        self.assertEqual(
            minutes.content,
            "Committee reviewed the submitted protocol.",
        )
        self.assertEqual(minutes.recorded_at, recorded_at)
        self.assertEqual(meeting.minutes, minutes)

def test_only_one_minutes_per_meeting(self):
    tenant = Tenant.objects.create(
        code="must",
        name="MUST",
    )

    chair = User.objects.create_user(
        email="chair@example.com",
        password="password123",
    )

    meeting = Meeting.objects.create(
        tenant=tenant,
        title="IRB Committee Meeting",
        meeting_date=timezone.now(),
        chair=chair,
    )

    MeetingMinutes.objects.create(
        tenant=tenant,
        meeting=meeting,
        content="First version of meeting minutes.",
        recorded_at=timezone.now(),
    )

    with self.assertRaises(IntegrityError):
        MeetingMinutes.objects.create(
            tenant=tenant,
            meeting=meeting,
            content="Second version of meeting minutes.",
            recorded_at=timezone.now(),
        )


class MeetingParticipantModelTest(TestCase):

    def test_create_participant(self):
        tenant = Tenant.objects.create(
            code="must",
            name="MUST",
        )

        chair = User.objects.create_user(
            email="chair@example.com",
            password="password123",
        )

        reviewer = User.objects.create_user(
            email="reviewer@example.com",
            password="password123",
        )

        meeting = Meeting.objects.create(
            tenant=tenant,
            title="IRB Committee Meeting",
            meeting_date=timezone.now(),
            chair=chair,
        )

        participant = MeetingParticipant.objects.create(
            meeting=meeting,
            user=reviewer,
            role=ParticipantRole.REVIEWER,
        )

        self.assertEqual(participant.role, ParticipantRole.REVIEWER)
        self.assertEqual(participant.meeting, meeting)
        self.assertEqual(participant.user, reviewer)

class MeetingAgendaModelTest(TestCase):

    def test_create_agenda_item(self):
        tenant = Tenant.objects.create(
            code="must",
            name="MUST",
        )

        chair = User.objects.create_user(
            email="chair@example.com",
            password="password123",
        )

        meeting = Meeting.objects.create(
            tenant=tenant,
            title="IRB Meeting",
            meeting_date=timezone.now(),
            chair=chair,
        )

        protocol = Protocol.objects.create(
            tenant=tenant,
            title="Cancer Study",
            protocol_number="IRB-001",
            principal_investigator=chair,
            risk_level=RiskLevel.LOW,
        )

        agenda = MeetingAgenda.objects.create(
            meeting=meeting,
            protocol=protocol,
            order=1,
            presenter=chair,
        )

        self.assertEqual(agenda.order, 1)
        self.assertEqual(agenda.meeting, meeting)
        self.assertEqual(agenda.protocol, protocol)

class MeetingVoteModelTest(TestCase):

    def test_create_vote(self):
        tenant = Tenant.objects.create(
            code="must",
            name="MUST",
        )

        chair = User.objects.create_user(
            email="chair@example.com",
            password="password123",
        )

        reviewer = User.objects.create_user(
            email="reviewer@example.com",
            password="password123",
        )

        meeting = Meeting.objects.create(
            tenant=tenant,
            title="IRB Committee Meeting",
            meeting_date=timezone.now(),
            chair=chair,
        )

        protocol = Protocol.objects.create(
            tenant=tenant,
            title="Cancer Study",
            protocol_number="IRB-001",
            principal_investigator=chair,
            risk_level=RiskLevel.LOW,
        )

        participant = MeetingParticipant.objects.create(
            meeting=meeting,
            user=reviewer,
            role=ParticipantRole.REVIEWER,
        )

        agenda = MeetingAgenda.objects.create(
            meeting=meeting,
            protocol=protocol,
            order=1,
            presenter=chair,
        )

        vote = MeetingVote.objects.create(
            agenda=agenda,
            participant=participant,
            vote=VoteChoice.APPROVE,
            comment="Looks good.",
        )

        self.assertEqual(vote.vote, VoteChoice.APPROVE)
        self.assertEqual(vote.participant, participant)
        self.assertEqual(vote.agenda, agenda)
        self.assertEqual(vote.comment, "Looks good.")
