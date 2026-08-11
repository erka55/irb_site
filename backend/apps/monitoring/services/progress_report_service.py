from django.utils import timezone

from apps.monitoring.models import (
    ProgressReport,
    ProgressReportStatus,
)
from common.events.memory import InMemoryEventPublisher
from common.events.monitoring import ProgressReportSubmitted


class ProgressReportService:

    publisher = InMemoryEventPublisher()

    @staticmethod
    def submit_report(
        report: ProgressReport,
    ) -> ProgressReport:

        if report.status != ProgressReportStatus.DRAFT:
            raise ValueError(
                "Only draft reports can be submitted."
            )

        report.status = ProgressReportStatus.SUBMITTED
        report.submitted_at = timezone.now()

        report.save(
            update_fields=[
                "status",
                "submitted_at",
                "updated_at",
            ]
        )

        ProgressReportService.publisher.publish(
            ProgressReportSubmitted(
                tenant_id=report.tenant_id,
                actor_id=report.submitted_by_id,
                protocol_id=report.protocol_id,
                progress_report_id=report.pk,
            )
        )

        return report
