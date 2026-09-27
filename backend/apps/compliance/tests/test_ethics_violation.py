from django.test import TestCase

from apps.compliance.models import EthicsViolation
from apps.compliance.services.ethics_violation_service import (
    EthicsViolationService,
)
from apps.core.models import RoleChoices
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import Membership, User


class EthicsViolationServiceTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="T301",
            name="Ethics Violation Tenant",
        )

        self.other_tenant = Tenant.objects.create(
            code="T302",
            name="Other Ethics Tenant",
        )

        self.user = User.objects.create_user(
            email="ethics@example.com",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            email="other-ethics@example.com",
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
            title="Ethics Test Protocol",
            protocol_number="IRB-ETHICS-001",
            principal_investigator=self.user,
            risk_level=RiskLevel.LOW,
            summary="Ethics violation test protocol",
        )

        self.other_protocol = Protocol.objects.create(
            tenant=self.other_tenant,
            title="Other Ethics Protocol",
            protocol_number="IRB-ETHICS-002",
            principal_investigator=self.other_user,
            risk_level=RiskLevel.LOW,
            summary="Other ethics violation protocol",
        )

    def test_record_creates_ethics_violation(self):
        violation = EthicsViolationService.record(
            tenant=self.tenant,
            protocol=self.protocol,
            violation_type=EthicsViolation.ViolationType.DATA_FALSIFICATION,
            description="Research data was found to have been falsified.",
        )

        self.assertIsNotNone(violation.pk)
        self.assertEqual(violation.tenant, self.tenant)
        self.assertEqual(violation.protocol, self.protocol)
        self.assertEqual(
            violation.violation_type,
            EthicsViolation.ViolationType.DATA_FALSIFICATION,
        )
        self.assertEqual(
            violation.description,
            "Research data was found to have been falsified.",
        )

        self.assertEqual(
            EthicsViolation.objects.count(),
            1,
        )

    def test_record_rejects_protocol_from_different_tenant(self):
        with self.assertRaisesMessage(
            ValueError,
            "Protocol belongs to a different tenant.",
        ):
            EthicsViolationService.record(
                tenant=self.tenant,
                protocol=self.other_protocol,
                violation_type=EthicsViolation.ViolationType.DATA_FALSIFICATION,
                description="Violation description.",
            )

        self.assertFalse(
            EthicsViolation.objects.exists()
        )

    def test_record_rejects_blank_description(self):
        with self.assertRaisesMessage(
            ValueError,
            "Description is required.",
        ):
            EthicsViolationService.record(
                tenant=self.tenant,
                protocol=self.protocol,
                violation_type=EthicsViolation.ViolationType.DATA_FALSIFICATION,
                description="   ",
            )

        self.assertFalse(
            EthicsViolation.objects.exists()
        )

    def test_record_strips_description(self):
        violation = EthicsViolationService.record(
            tenant=self.tenant,
            protocol=self.protocol,
            violation_type=EthicsViolation.ViolationType.CONFIDENTIALITY_BREACH,
            description="  Confidentiality breach occurred.  ",
        )

        self.assertEqual(
            violation.description,
            "Confidentiality breach occurred.",
        )

    def test_record_rejects_invalid_violation_type(self):
        with self.assertRaisesMessage(
            ValueError,
            "Invalid ethics violation type.",
        ):
            EthicsViolationService.record(
                tenant=self.tenant,
                protocol=self.protocol,
                violation_type="INVALID_TYPE",
                description="Violation description.",
            )

        self.assertFalse(
            EthicsViolation.objects.exists()
        )
