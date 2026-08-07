from unittest.mock import MagicMock, patch

from django.test import TestCase

from apps.decision.models.letter import PublicationStatus
from apps.decision.services.publication_service import (
    DecisionPublicationService,
)

class DecisionPublicationServiceTest(TestCase):

    def _decision(self):
        decision = MagicMock()

        decision.pk = "decision-001"
        decision.protocol_id = "protocol-001"

        decision.protocol.id = "protocol-001"
        decision.protocol.tenant_id = "tenant-001"
        decision.protocol.title = "Test Research Protocol"

        return decision

    def _letter(self):
        letter = MagicMock()

        letter.pk = 1
        letter.decision_id = "decision-001"
        letter.publication_status = PublicationStatus.GENERATED
        letter.letter_number = None

        return letter

    @patch(
        "apps.decision.services.publication_service.Letter.objects.create"
    )
    @patch(
        "apps.decision.services.publication_service.DecisionPublicationService.publisher"
    )
    def test_generate_letter(
        self,
        mock_publisher,
        mock_create,
    ):
        decision = self._decision()
        letter = self._letter()

        mock_create.return_value = letter

        result = DecisionPublicationService.generate_letter(
            decision
        )

        self.assertEqual(result, letter)

        mock_create.assert_called_once_with(
            decision=decision,
            title="IRB Decision - Test Research Protocol",
            content="",
            rendered_content="",
            publication_status=PublicationStatus.GENERATED,
        )

        mock_publisher.publish.assert_called_once()

    @patch(
        "apps.decision.services.publication_service.DecisionPublicationService.publisher"
    )
    @patch(
        "apps.decision.services.publication_service.timezone.now"
    )
    def test_publish_decision(
        self,
        mock_now,
        mock_publisher,
    ):
        decision = self._decision()
        letter = self._letter()

        published_by = MagicMock()
        published_by.pk = "user-001"

        published_at = MagicMock()
        mock_now.return_value = published_at

        decision.letters.order_by.return_value.first.return_value = letter

        result = DecisionPublicationService.publish(
            decision,
            published_by,
        )

        self.assertEqual(result, letter)
        self.assertEqual(
            letter.publication_status,
            PublicationStatus.PUBLISHED,
        )
        self.assertEqual(
            letter.published_at,
            published_at,
        )
        self.assertEqual(
            letter.published_by,
            published_by,
        )

        self.assertTrue(letter.letter_number.startswith("IRB-"))

        letter.save.assert_called_once()

        mock_publisher.publish.assert_called_once()

    @patch(
        "apps.decision.services.publication_service.DecisionPublicationService.publisher"
    )
    def test_publish_requires_generated_letter(
        self,
        mock_publisher,
    ):
        decision = self._decision()

        decision.letters.order_by.return_value.first.return_value = None

        with self.assertRaises(ValueError):
            DecisionPublicationService.publish(
                decision,
                MagicMock(),
            )

        mock_publisher.publish.assert_not_called()

    @patch(
        "apps.decision.services.publication_service.DecisionPublicationService.publisher"
    )
    def test_publish_rejects_already_published_letter(
        self,
        mock_publisher,
    ):
        decision = self._decision()
        letter = self._letter()

        letter.publication_status = PublicationStatus.PUBLISHED

        decision.letters.order_by.return_value.first.return_value = letter

        with self.assertRaises(ValueError):
            DecisionPublicationService.publish(
                decision,
                MagicMock(),
            )

        mock_publisher.publish.assert_not_called()

    @patch(
        "apps.decision.services.publication_service.DecisionPublicationService.publisher"
    )
    def test_issue_letter_requires_published_status(
        self,
        mock_publisher,
    ):
        letter = self._letter()

        letter.publication_status = PublicationStatus.GENERATED

        with self.assertRaises(ValueError):
            DecisionPublicationService.issue_letter(
                letter
            )

        mock_publisher.publish.assert_not_called()

    @patch(
        "apps.decision.services.publication_service.DecisionPublicationService.publisher"
    )
    def test_issue_published_letter(
        self,
        mock_publisher,
    ):
        letter = self._letter()

        letter.publication_status = PublicationStatus.PUBLISHED

        letter.decision.protocol.tenant_id = "tenant-001"
        letter.decision.protocol_id = "protocol-001"
        letter.decision_id = "decision-001"

        actor = MagicMock()
        actor.pk = "user-001"

        result = DecisionPublicationService.issue_letter(
            letter,
            actor=actor,
        )

        self.assertEqual(result, letter)

        mock_publisher.publish.assert_called_once()
