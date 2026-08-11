from datetime import timedelta

from django.utils import timezone

from apps.monitoring.models import (
    IncidentReport,
    IncidentReportStatus,
)
from common.events.incident import IncidentReportSubmitted
from common.events.memory import InMemoryEventPublisher


class IncidentReportService:

    MAX_REPORTING_DELAY = timedelta(hours=48)

    publisher = InMemoryEventPublisher()

    @classmethod
    def record_reported_at(
        cls,
        report: IncidentReport,
        reported_at=None,
    ) -> IncidentReport:

        if report.reported_at is not None:
            raise ValueError(
                "Incident report has already been reported."
            )

        reported_at = reported_at or timezone.now()

        if reported_at - report.occurred_at > cls.MAX_REPORTING_DELAY:
            raise ValueError(
                "Incident must be reported within 48 hours."
            )

        if reported_at < report.occurred_at:
            raise ValueError(
                "Reported time cannot be before occurred time."
            )

        report.reported_at = reported_at
        report.status = IncidentReportStatus.SUBMITTED

        report.save(
            update_fields=[
                "reported_at",
                "status",
                "updated_at",
            ]
        )

        cls.publisher.publish(
            IncidentReportSubmitted(
                tenant_id=report.tenant_id,
                actor_id=report.reported_by_id,
                protocol_id=report.protocol_id,
                incident_report_id=report.pk,
            )
        )

        return report
