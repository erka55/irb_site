from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.compliance.models import ConflictOfInterestDeclaration
from apps.compliance.services.coi_service import (
    ConflictOfInterestDeclarationService,
)
from apps.core.models import RoleChoices
from apps.protocols.models import Protocol
from apps.protocols.enums import RiskLevel
from apps.tenants.models import Tenant
from apps.users.models import Membership, User


class ConflictOfInterestDeclarationServiceTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="T001",
            name="Test Tenant",
        )

        self.other_tenant = Tenant.objects.create(
            code="T002",
            name="Other Tenant",
        )

        self.declarant = User.objects.create_user(
            email="declarant@example.com",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="test-password",
        )

        Membership.objects.create(
            user=self.declarant,
            tenant=self.tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Test Protocol",
            protocol_number="IRB-TEST-001",
            principal_investigator=self.declarant,
            risk_level=RiskLevel.LOW,
            summary="Test protocol summary",
        )

        self.other_protocol = Protocol.objects.create(
            tenant=self.other_tenant,
            title="Other Protocol",
            protocol_number="IRB-TEST-002",
            principal_investigator=self.other_user,
            risk_level=RiskLevel.LOW,
            summary="Other protocol summary",
        )

    def test_declare_creates_declaration(self):
        declared_at = timezone.now()

        declaration = ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=declared_at,
            signature_reference="signature/ref/001",
        )

        self.assertIsNotNone(declaration.pk)
        self.assertEqual(declaration.tenant, self.tenant)
        self.assertEqual(declaration.protocol, self.protocol)
        self.assertEqual(declaration.declarant, self.declarant)
        self.assertEqual(declaration.conflict_types, ["financial"])
        self.assertEqual(
            declaration.description,
            "Financial relationship with the research sponsor.",
        )
        self.assertEqual(declaration.declared_at, declared_at)
        self.assertEqual(
            declaration.signature_reference,
            "signature/ref/001",
        )

        self.assertEqual(
            ConflictOfInterestDeclaration.objects.count(),
            1,
        )

    def test_declare_rejects_protocol_from_different_tenant(self):
        with self.assertRaisesMessage(
            ValueError,
            "Protocol belongs to a different tenant.",
        ):
            ConflictOfInterestDeclarationService.declare(
                tenant=self.tenant,
                protocol=self.other_protocol,
                declarant=self.declarant,
                conflict_types=["financial"],
                description="Conflict description.",
                declared_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestDeclaration.objects.exists()
        )

    def test_declare_rejects_declarant_without_active_membership(self):
        inactive_user = User.objects.create_user(
            email="inactive@example.com",
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
            "Declarant does not have an active membership in the tenant.",
        ):
            ConflictOfInterestDeclarationService.declare(
                tenant=self.tenant,
                protocol=self.protocol,
                declarant=inactive_user,
                conflict_types=["financial"],
                description="Conflict description.",
                declared_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestDeclaration.objects.exists()
        )

    def test_declare_rejects_declarant_from_different_tenant(self):
        Membership.objects.create(
            user=self.other_user,
            tenant=self.other_tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        with self.assertRaisesMessage(
            ValueError,
            "Declarant does not have an active membership in the tenant.",
        ):
            ConflictOfInterestDeclarationService.declare(
                tenant=self.tenant,
                protocol=self.protocol,
                declarant=self.other_user,
                conflict_types=["financial"],
                description="Conflict description.",
                declared_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestDeclaration.objects.exists()
        )

    def test_declare_rejects_non_list_conflict_types(self):
        with self.assertRaisesMessage(
            ValueError,
            "conflict_types must be a list.",
        ):
            ConflictOfInterestDeclarationService.declare(
                tenant=self.tenant,
                protocol=self.protocol,
                declarant=self.declarant,
                conflict_types="financial",
                description="Conflict description.",
                declared_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestDeclaration.objects.exists()
        )

    def test_declare_rejects_blank_description(self):
        with self.assertRaisesMessage(
            ValueError,
            "Description is required.",
        ):
            ConflictOfInterestDeclarationService.declare(
                tenant=self.tenant,
                protocol=self.protocol,
                declarant=self.declarant,
                conflict_types=["financial"],
                description="   ",
                declared_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestDeclaration.objects.exists()
        )

    def test_declare_strips_description(self):
        declaration = ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="  Conflict description.  ",
            declared_at=timezone.now(),
        )

        self.assertEqual(
            declaration.description,
            "Conflict description.",
        )

    def test_has_conflict_returns_true_for_declared_protocol_and_user(self):
        ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=timezone.now(),
        )

        self.assertTrue(
            ConflictOfInterestDeclarationService.has_conflict(
                protocol=self.protocol,
                declarant=self.declarant,
            )
        )

    def test_has_conflict_returns_false_without_declaration(self):
        self.assertFalse(
            ConflictOfInterestDeclarationService.has_conflict(
                protocol=self.protocol,
                declarant=self.declarant,
            )
        )

    def test_has_conflict_is_scoped_to_protocol_and_declarant(self):
        ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=timezone.now(),
        )

        self.assertFalse(
            ConflictOfInterestDeclarationService.has_conflict(
                protocol=self.protocol,
                declarant=self.other_user,
            )
        )

        self.assertFalse(
            ConflictOfInterestDeclarationService.has_conflict(
                protocol=self.other_protocol,
                declarant=self.declarant,
            )
        )

    def test_can_participate_in_vote_returns_false_with_conflict(self):
        ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=timezone.now(),
        )

        self.assertFalse(
            ConflictOfInterestDeclarationService.can_participate_in_vote(
                protocol=self.protocol,
                declarant=self.declarant,
            )
        )

    def test_can_participate_in_vote_returns_true_without_conflict(self):
        self.assertTrue(
            ConflictOfInterestDeclarationService.can_participate_in_vote(
                protocol=self.protocol,
                declarant=self.declarant,
            )
        )
