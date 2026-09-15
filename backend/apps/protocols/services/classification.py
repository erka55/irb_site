from django.db import transaction
from django.utils import timezone

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

        return ClassificationAssessment.objects.create(
            tenant=protocol_version.protocol.tenant,
            protocol=protocol_version.protocol,
            protocol_version=protocol_version,
            classification=classification,
            evaluated_at=timezone.now(),
            evaluated_by=evaluated_by,
            rationale=rationale,
        )
