import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.decision.models.decision import Decision
from apps.protocols.models import Protocol
from apps.protocols.enums import ProtocolStatus, RiskLevel
from apps.tenants.models import Tenant
from apps.users.models import User


class DecisionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(code="t1", name="Test Tenant")
        cls.pi = User.objects.create_user(email="pi@example.com", password="x")
        cls.chair = User.objects.create_user(email="chair@example.com", password="x")
        cls.protocol = Protocol.objects.create(
            tenant=cls.tenant,
            title="Test Protocol",
            protocol_number="P-0001",
            principal_investigator=cls.pi,
            risk_level=RiskLevel.LOW,
            status=ProtocolStatus.UNDER_REVIEW,
        )

    def _make_decision(self, **overrides):
        defaults = dict(
            tenant=self.tenant,
            protocol=self.protocol,
            decided_by=self.chair,
            decision_type=Decision.DecisionType.APPROVED,
            quorum_met=True,
        )
        defaults.update(overrides)
        return Decision(**defaults)

    def test_decision_requires_quorum(self):
        """BR-004: Decision cannot be issued without quorum."""
        decision = self._make_decision(quorum_met=False)
        with self.assertRaises(ValidationError):
            decision.save()

    def test_decision_saves_with_quorum(self):
        decision = self._make_decision(quorum_met=True)
        decision.save()
        self.assertIsNotNone(decision.pk)

    def test_decision_not_published_by_default(self):
        decision = self._make_decision()
        decision.save()
        self.assertFalse(decision.is_published)
        self.assertIsNone(decision.published_at)

    def test_published_decision_is_immutable(self):
        """BR-005 / BR-007: published decisions cannot be modified."""
        decision = self._make_decision()
        decision.save()

        decision.is_published = True
        decision.save()

        decision.quorum_met = False
        with self.assertRaises(ValueError):
            decision.save()

    def test_unpublished_decision_can_be_modified(self):
        decision = self._make_decision()
        decision.save()

        decision.decision_type = Decision.DecisionType.REJECTED
        decision.save()  # алдаа гарахгүй байх ёстой

        decision.refresh_from_db()
        self.assertEqual(decision.decision_type, Decision.DecisionType.REJECTED)

    def test_all_four_decision_types_valid(self):
        for choice in Decision.DecisionType.values:
            with self.subTest(choice=choice):
                decision = self._make_decision(decision_type=choice)
                decision.save()
                self.assertEqual(decision.decision_type, choice)
