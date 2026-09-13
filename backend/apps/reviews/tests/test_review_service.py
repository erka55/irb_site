from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.audit.models import AuditLog
from apps.protocols.enums import ProtocolStatus, RiskLevel
from apps.protocols.models import Protocol
from apps.reviews.models import Review, ReviewRecommendation, ReviewStatus
from apps.reviews.services.review_service import ReviewService
from apps.tenants.models import Tenant
from apps.users.models import User
from common.events.types import EventTypes


class ReviewServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(
            code="t1",
            name="Test Tenant",
        )
        cls.pi = User.objects.create_user(
            email="pi@example.com",
            password="x",
        )
        cls.reviewer = User.objects.create_user(
            email="reviewer@example.com",
            password="x",
        )

        cls.protocol = Protocol.objects.create(
            tenant=cls.tenant,
            title="Test Protocol",
            protocol_number="P-REVIEW-001",
            principal_investigator=cls.pi,
            risk_level=RiskLevel.LOW,
            status=ProtocolStatus.UNDER_REVIEW,
        )

        cls.review = Review.objects.create(
            protocol_id=cls.protocol.id,
            reviewer_id=cls.reviewer.id,
            status=ReviewStatus.ASSIGNED,
            due_date=timezone.now() + timedelta(days=7),
        )

    def test_submit_review_creates_tenant_scoped_audit_log(self):
        ReviewService.submit_review(
            review=self.review,
            recommendation=ReviewRecommendation.APPROVE,
            score=4.5,
            comments="Good study.",
        )

        log = AuditLog.objects.filter(
            entity_type="review",
            entity_id=self.review.id,
        ).first()

        self.assertIsNotNone(log)
        self.assertEqual(
            log.action,
            EventTypes.REVIEW_COMPLETED,
        )
        self.assertEqual(
            log.tenant,
            self.tenant,
        )
        self.assertEqual(
            log.actor,
            self.reviewer,
        )
