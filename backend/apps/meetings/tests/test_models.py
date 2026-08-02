from django.test import TestCase
from django.utils import timezone

from apps.meetings.models import (
    Meeting,
    MeetingParticipant,
    ParticipantRole,
)
from apps.tenants.models import Tenant
from apps.users.models import User


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
