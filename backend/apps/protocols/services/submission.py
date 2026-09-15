from django.db import transaction
from django.utils import timezone

from apps.protocols.enums import SubmissionStatus
from apps.protocols.models import ProtocolSubmission
from common.events.factory import get_event_publisher
from common.events.submission import SubmissionResubmitted


class ProtocolSubmissionService:

    @staticmethod
    def mark_incomplete(
        submission,
        reason,
    ):
        if submission.status != SubmissionStatus.RECEIVED:
            raise ValueError(
                "Only received submissions can be marked incomplete."
            )

        if not reason:
            raise ValueError(
                "Incomplete reason is required."
            )

        submission.status = SubmissionStatus.INCOMPLETE
        submission.incomplete_reason = reason
        submission.save(
            update_fields=[
                "status",
                "incomplete_reason",
                "updated_at",
            ],
        )

        return submission

    @staticmethod
    def mark_complete(
        submission,
    ):
        if submission.status != SubmissionStatus.RECEIVED:
            raise ValueError(
                "Only received submissions can be marked complete."
            )

        submission.status = SubmissionStatus.COMPLETE
        submission.incomplete_reason = ""
        submission.save(
            update_fields=[
                "status",
                "incomplete_reason",
                "updated_at",
            ],
        )

        return submission

    @staticmethod
    @transaction.atomic
    def resubmit(
        submission,
        resubmitted_by,
    ):
        if submission.status != SubmissionStatus.INCOMPLETE:
            raise ValueError(
                "Only incomplete submissions can be resubmitted."
            )

        submission.status = SubmissionStatus.RECEIVED
        submission.incomplete_reason = ""
        submission.closed_at = None
        submission.save(
            update_fields=[
                "status",
                "incomplete_reason",
                "closed_at",
                "updated_at",
            ],
        )

        event = SubmissionResubmitted(
            tenant_id=submission.tenant_id,
            actor_id=resubmitted_by.id,
            submission_id=submission.id,
            protocol_id=submission.protocol_id,
        )

        get_event_publisher().publish(event)

        return submission

    @staticmethod
    def close(
        submission,
    ):
        if submission.status != SubmissionStatus.INCOMPLETE:
            raise ValueError(
                "Only incomplete submissions can be closed."
            )

        submission.status = SubmissionStatus.CLOSED
        submission.closed_at = timezone.now()

        submission.save(
            update_fields=[
                "status",
                "closed_at",
                "updated_at",
            ],
        )

        return submission
