from datetime import date

from django.test import TestCase

from apps.decision.enums import DecisionType
from apps.decision.models import Decision, DecisionCondition
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import User


class DecisionConditionTest(TestCase):

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
            decision_type=DecisionType.APPROVED_WITH_CONDITIONS,
            decision_date=date.today(),
            rationale="Needs revisions",
            created_by=self.user,
        )

    def test_create_condition(self):
        condition = DecisionCondition.objects.create(
            decision=self.decision,
            description="Revise consent form",
            order=1,
        )

        self.assertEqual(condition.decision, self.decision)
        self.assertEqual(condition.order, 1)
