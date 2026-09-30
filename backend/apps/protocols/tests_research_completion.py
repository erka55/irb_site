from datetime import datetime, timezone
from django.test import TestCase

from apps.core.models import RoleChoices
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol, ResearchCompletion
from apps.protocols.services.research_completion import (
    ResearchCompletionService,
)
from apps.tenants.models import Tenant
from apps.users.models import Membership, User


class ResearchCompletionServiceTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="T401",
            name="Research Completion Tenant",
        )

        self.other_tenant = Tenant.objects.create(
            code="T402",
            name="Other Research Tenant",
        )

        self.user = User.objects.create_user(
            email="research@example.com",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            email="other-research@example.com",
            password="test-password",
        )

        Membership.objects.create(
            user=self.user,
            tenant=self.tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        Membership.objects.create(
            user=self.other_user,
            tenant=self.other_tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Research Completion Protocol",
            protocol_number="IRB-COMP-001",
            principal_investigator=self.user,
            risk_level=RiskLevel.LOW,
            summary="Research completion test protocol",
        )

        self.other_protocol = Protocol.objects.create(
            tenant=self.other_tenant,
            title="Other Research Protocol",
            protocol_number="IRB-COMP-002",
            principal_investigator=self.other_user,
            risk_level=RiskLevel.LOW,
            summary="Other research protocol",
        )

    def test_record_creates_research_completion(self):
        completed_at = datetime(
            2026,
            9,
            29,
            10,
            0,
            tzinfo=timezone.utc,
        )

        completion = ResearchCompletionService.record(
            tenant=self.tenant,
            protocol=self.protocol,
            recorded_by=self.user,
            completed_at=completed_at,
        )

        self.assertIsNotNone(completion.pk)
        self.assertEqual(completion.tenant, self.tenant)
        self.assertEqual(completion.protocol, self.protocol)
        self.assertEqual(completion.recorded_by, self.user)

        self.assertEqual(
            ResearchCompletion.objects.count(),
            1,
        )

    def test_record_rejects_protocol_from_different_tenant(self):
        with self.assertRaisesMessage(
            ValueError,
            "Protocol belongs to a different tenant.",
        ):
            ResearchCompletionService.record(
                tenant=self.tenant,
                protocol=self.other_protocol,
                recorded_by=self.user,
                completed_at="2026-09-29T10:00:00Z",
            )

        self.assertFalse(
            ResearchCompletion.objects.exists()
        )

    def test_record_rejects_inactive_or_missing_membership(self):
        inactive_user = User.objects.create_user(
            email="inactive-research@example.com",
            password="test-password",
        )

        Membership.objects.create(
            user=inactive_user,
            tenant=self.tenant,
            role=RoleChoices.REVIEWER,
            is_active=False,
        )

        with self.assertRaisesMessage(
            ValueError,
            "Recorder does not have an active membership "
            "in the tenant.",
        ):
            ResearchCompletionService.record(
                tenant=self.tenant,
                protocol=self.protocol,
                recorded_by=inactive_user,
                completed_at="2026-09-29T10:00:00Z",
            )

        self.assertFalse(
            ResearchCompletion.objects.exists()
        )

    def test_record_rejects_missing_completed_at(self):
        with self.assertRaisesMessage(
            ValueError,
            "Completed time is required.",
        ):
            ResearchCompletionService.record(
                tenant=self.tenant,
                protocol=self.protocol,
                recorded_by=self.user,
                completed_at=None,
            )

        self.assertFalse(
            ResearchCompletion.objects.exists()
        )

    def test_record_rejects_duplicate_completion(self):
        ResearchCompletionService.record(
            tenant=self.tenant,
            protocol=self.protocol,
            recorded_by=self.user,
            completed_at="2026-09-29T10:00:00Z",
        )

        with self.assertRaisesMessage(
            ValueError,
            "Research completion has already been recorded.",
        ):
            ResearchCompletionService.record(
                tenant=self.tenant,
                protocol=self.protocol,
                recorded_by=self.user,
                completed_at="2026-09-30T10:00:00Z",
            )

        self.assertEqual(
            ResearchCompletion.objects.count(),
            1,
        )
