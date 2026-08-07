from django.db import transaction
from django.utils import timezone

from apps.decision.models.decision import Decision
from apps.decision.models.letter import Letter, PublicationStatus
from common.events.decision import (
    DecisionLetterGenerated,
    DecisionLetterIssued,
    DecisionPublished,
)
from common.events.memory import InMemoryEventPublisher


class DecisionPublicationService:
    """
    Handles decision publication workflow.

    Responsibilities:
    - Generate official decision letter
    - Publish decision
    - Issue decision letter
    - Publish corresponding domain events
    """

    publisher = InMemoryEventPublisher()

    @classmethod
    @transaction.atomic
    def generate_letter(cls, decision: Decision, actor=None) -> Letter:
        """
        Generate an official decision letter.
        """

        letter = Letter.objects.create(
            decision=decision,
            title=f"IRB Decision - {decision.protocol.title}",
            content="",
            rendered_content="",
            publication_status=PublicationStatus.GENERATED,
        )

        cls.publisher.publish(
            DecisionLetterGenerated(
                tenant_id=decision.protocol.tenant_id,
                actor_id=actor.pk if actor else None,
                protocol_id=decision.protocol_id,
                decision_id=decision.pk,
                letter_id=letter.pk,
            )
        )

        return letter

    @classmethod
    @transaction.atomic
    def publish(
        cls,
        decision: Decision,
        published_by,
    ) -> Letter:
        """
        Publish the generated decision letter.
        """

        letter = (
            decision.letters
            .order_by("-created_at")
            .first()
        )

        if letter is None:
            raise ValueError(
                "Decision letter has not been generated."
            )

        if letter.publication_status == PublicationStatus.PUBLISHED:
            raise ValueError(
                "Decision letter is already published."
            )

        if not letter.letter_number:
            year = timezone.now().year
            letter.letter_number = (
                f"IRB-{year}-{letter.pk:05d}"
            )

        letter.publication_status = PublicationStatus.PUBLISHED
        letter.published_at = timezone.now()
        letter.published_by = published_by

        letter.save(
            update_fields=[
                "letter_number",
                "publication_status",
                "published_at",
                "published_by",
                "updated_at",
            ]
        )

        cls.publisher.publish(
            DecisionPublished(
                tenant_id=decision.protocol.tenant_id,
                actor_id=published_by.pk,
                protocol_id=decision.protocol_id,
                decision_id=decision.pk,
            )
        )

        return letter

    @classmethod
    @transaction.atomic
    def issue_letter(
        cls,
        letter: Letter,
        actor=None,
    ) -> Letter:
        """
        Issue a published decision letter.
        """

        if letter.publication_status != PublicationStatus.PUBLISHED:
            raise ValueError(
                "Only published letters can be issued."
            )

        cls.publisher.publish(
            DecisionLetterIssued(
                tenant_id=letter.decision.protocol.tenant_id,
                actor_id=actor.pk if actor else None,
                protocol_id=letter.decision.protocol_id,
                decision_id=letter.decision_id,
                letter_id=letter.pk,
            )
        )

        return letter
