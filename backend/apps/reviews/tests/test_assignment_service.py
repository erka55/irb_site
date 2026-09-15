from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.core.models.enums import RoleChoices
from apps.protocols.enums import ProtocolStatus, RiskLevel
from apps.protocols.models import Protocol
from apps.reviews.models import (
    AssignmentRole,
    Review,
    ReviewAssignment,
    ReviewStatus,
)
from apps.reviews.services.assignment_service import ReviewAssignmentService
from apps.tenants.models import Tenant
from apps.users.models import Membership, User


class ReviewAssignmentServiceTests(TestCase):

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

        Membership.objects.create(
            user=cls.reviewer,
            tenant=cls.tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        cls.protocol = Protocol.objects.create(
            tenant=cls.tenant,
            title="Test Protocol",
            protocol_number="P-ASSIGN-001",
            principal_investigator=cls.pi,
            risk_level=RiskLevel.LOW,
            status=ProtocolStatus.UNDER_REVIEW,
        )

    def test_assign_reviewer_creates_assignment_and_review(self):
        due_date = timezone.now() + timedelta(days=7)

        assignment, review = ReviewAssignmentService.assign_reviewer(
            protocol_id=self.protocol.id,
            reviewer_id=self.reviewer.id,
            due_date=due_date,
            role=AssignmentRole.PRIMARY,
        )

        self.assertEqual(
            assignment.tenant,
            self.tenant,
        )
        self.assertEqual(
            assignment.protocol,
            self.protocol,
        )
        self.assertEqual(
            assignment.reviewer,
            self.reviewer,
        )
        self.assertEqual(
            assignment.role,
            AssignmentRole.PRIMARY,
        )

        self.assertEqual(
            review.tenant,
            self.tenant,
        )
        self.assertEqual(
            review.protocol,
            self.protocol,
        )
        self.assertEqual(
            review.reviewer,
            self.reviewer,
        )
        self.assertEqual(
            review.status,
            ReviewStatus.ASSIGNED,
        )
        self.assertEqual(
            review.due_date,
            due_date,
        )

        self.assertEqual(
            ReviewAssignment.objects.count(),
            1,
        )
        self.assertEqual(
            Review.objects.count(),
            1,
        )
