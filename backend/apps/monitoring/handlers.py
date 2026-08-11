from django.utils import timezone

from common.events.base import BaseEvent

from apps.monitoring.services.monitoring_plan_service import (
    MonitoringPlanService,
)
from apps.protocols.models import Protocol


class MonitoringHandler:
    """
    Handles monitoring-related domain events.
    """

    @staticmethod
    def handle_decision_published(event: BaseEvent):
        """
        Create a monitoring plan when a decision is published.
        """

        protocol = Protocol.objects.get(
            id=event.payload["protocol_id"]
        )

        return MonitoringPlanService.create_plan(
            protocol=protocol,
            start_date=timezone.now().date(),
        )
