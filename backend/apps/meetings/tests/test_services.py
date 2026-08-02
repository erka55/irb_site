from django.test import TestCase
from django.utils import timezone

from apps.meetings.models import (
    Meeting,
    MeetingStatus,
)
from apps.meetings.services import MeetingService
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
