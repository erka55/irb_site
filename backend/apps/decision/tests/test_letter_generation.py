from datetime import date

from django.test import TestCase

from apps.decision.enums import DecisionType, LetterStatus
from apps.decision.models import Decision, DecisionLetter
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import User


class DecisionLetterTest(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="must",
            name="MUST",
        )

        self.user = User.objects.create_user(
            email="reviewer@test.mn",
            password="password123",
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="COVID Study",
            protocol_number="IRB-001",
            principal_investigator=self.user,
            risk_level=RiskLevel.LOW,
        )

        self.decision = Decision.objects.create(
            protocol=self.protocol,
            decision_type=DecisionType.APPROVED,
            decision_date=date.today(),
            rationale="Approved",
            created_by=self.user,
        )

    def test_create_letter(self):
        letter = DecisionLetter.objects.create(
            decision=self.decision,
            generated_by=self.user,
        )

        self.assertEqual(letter.status, LetterStatus.DRAFT)
        self.assertEqual(letter.version, 1)
        self.assertEqual(letter.decision, self.decision)
