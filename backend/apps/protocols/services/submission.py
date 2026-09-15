from django.utils import timezone
from apps.protocols.enums import SubmissionStatus
from apps.protocols.models import ProtocolSubmission


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
    def resubmit(
        submission,
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
    