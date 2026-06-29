from django.test import TestCase

from apps.audit.models import AuditLog
from apps.decision.models.decision import Decision
from apps.decision.services.decision_service import DecisionService
from apps.protocols.models import Protocol
from apps.protocols.enums import ProtocolStatus, RiskLevel
from apps.tenants.models import Tenant
from apps.users.models import User


class DecisionServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(code="t1", name="Test Tenant")
        cls.pi = User.objects.create_user(email="pi@example.com", password="x")
        cls.chair = User.objects.create_user(email="chair@example.com", password="x")
        cls.protocol = Protocol.objects.create(
            tenant=cls.tenant,
            title="Test Protocol",
            protocol_number="P-0002",
            principal_investigator=cls.pi,
            risk_level=RiskLevel.LOW,
            status=ProtocolStatus.UNDER_REVIEW,
        )
        cls.decision = Decision.objects.create(
            tenant=cls.tenant,
            protocol=cls.protocol,
            decided_by=cls.chair,
            decision_type=Decision.DecisionType.APPROVED,
            quorum_met=True,
        )

    def test_publish_sets_flags(self):
        DecisionService.publish_decision(decision=self.decision, actor=self.chair)
        self.decision.refresh_from_db()
        self.assertTrue(self.decision.is_published)
        self.assertIsNotNone(self.decision.published_at)

    def test_publish_creates_audit_log(self):
        DecisionService.publish_decision(decision=self.decision, actor=self.chair)

        log = AuditLog.objects.filter(
            entity_type="Decision", entity_id=self.decision.id
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.action, "decision.publish")
        self.assertEqual(log.actor, self.chair)
        self.assertEqual(log.payload["decision_type"], Decision.DecisionType.APPROVED)

    def test_cannot_publish_twice(self):
        DecisionService.publish_decision(decision=self.decision, actor=self.chair)
        with self.assertRaises(ValueError):
            DecisionService.publish_decision(decision=self.decision, actor=self.chair)

    def test_audit_log_is_immutable(self):
        """Sanity check on apps.audit's own guarantee, since we depend on it."""
        DecisionService.publish_decision(decision=self.decision, actor=self.chair)
        log = AuditLog.objects.filter(
            entity_type="Decision", entity_id=self.decision.id
        ).first()

        log.action = "tampered"
        with self.assertRaises(ValueError):
            log.save()
