from django.db import transaction
from django.utils import timezone

from common.events.classification import ClassificationAssessed
from common.events.factory import get_event_publisher
from apps.protocols.models import ClassificationAssessment
from apps.protocols.rules.classification import ClassificationEvaluator
from apps.protocols.rules.classification_context import (
    ClassificationContextFactory,
)


class ClassificationService:

    @staticmethod
    @transaction.atomic
    def evaluate(*, protocol_version, evaluated_by):
        context = ClassificationContextFactory.from_snapshot(
            protocol_version.snapshot
        )

        classification = ClassificationEvaluator.evaluate(context)

        if classification is None:
            return None

        rationale = (
            f"Classification automatically determined as "
            f"{classification} based on the protocol version snapshot."
        )

        assessment = ClassificationAssessment.objects.create(
            tenant=protocol_version.protocol.tenant,
            protocol=protocol_version.protocol,
            protocol_version=protocol_version,
            classification=classification,
            evaluated_at=timezone.now(),
            evaluated_by=evaluated_by,
            rationale=rationale,
        )

        publisher = get_event_publisher()

        publisher.publish(
            ClassificationAssessed(
                tenant_id=str(protocol_version.protocol.tenant_id),
                actor_id=str(evaluated_by.id) if evaluated_by else None,
                assessment_id=assessment.id,
                protocol_id=protocol_version.protocol_id,
                protocol_version_id=protocol_version.id,
                classification=classification,
            )
        )

        return assessment
