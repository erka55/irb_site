from django.test import TestCase
from apps.tenants.models import Tenant
from apps.users.models import User
from apps.meetings.models import Meeting


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
