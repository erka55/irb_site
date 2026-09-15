from datetime import datetime

from django.db import transaction

from apps.protocols.enums import (
    PreliminaryCheckResult,
    SubmissionStatus,
)
from apps.protocols.models import PreliminaryCheck
from apps.protocols.rules.completeness import (
    SubmissionCompletenessContext,
    SubmissionCompletenessEvaluator,
)
from apps.protocols.rules.working_days import WorkingDayRules
from apps.protocols.services.submission import ProtocolSubmissionService


class PreliminaryCheckService:

    @staticmethod
    @transaction.atomic
    def check(
        *,
        submission,
        checked_by,
        checked_at,
        context: SubmissionCompletenessContext,
    ):
        if submission.status != SubmissionStatus.RECEIVED:
            raise ValueError(
                "Only received submissions can undergo a preliminary check."
            )

        uploaded_document_types = set(
            submission.documents.values_list(
                "document_type",
                flat=True,
            )
        )

        completeness_result = SubmissionCompletenessEvaluator.evaluate(
            uploaded_document_types=uploaded_document_types,
            context=context,
        )

        missing_document_types = sorted(
            document_type.value
            for document_type in completeness_result.missing_document_types
        )

        correction_due_at = None

        if completeness_result.is_complete:
            result = PreliminaryCheckResult.COMPLETE

            ProtocolSubmissionService.mark_complete(
                submission,
            )

        else:
            result = PreliminaryCheckResult.INCOMPLETE

            correction_due_date = WorkingDayRules.add_working_days(
                checked_at.date(),
                WorkingDayRules.CORRECTION_PERIOD_DAYS,
            )

            correction_due_at = datetime.combine(
                correction_due_date,
                checked_at.timetz(),
            )

            ProtocolSubmissionService.mark_incomplete(
                submission,
                reason="Missing required submission documents.",
            )

        return PreliminaryCheck.objects.create(
            tenant=submission.tenant,
            submission=submission,
            checked_by=checked_by,
            checked_at=checked_at,
            result=result,
            missing_document_types=missing_document_types,
            correction_due_at=correction_due_at,
        )
