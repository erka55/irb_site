from apps.protocols.models import Protocol, ResearchCompletion
from apps.users.models import Membership

from common.events.factory import get_event_publisher
from common.events.research import ResearchCompleted


class ResearchCompletionService:

    @staticmethod
    def record(
        *,
        tenant,
        protocol: Protocol,
        recorded_by,
        completed_at,
    ) -> ResearchCompletion:

        if protocol.tenant_id != tenant.id:
            raise ValueError(
                "Protocol belongs to a different tenant."
            )

        if not Membership.objects.filter(
            user_id=recorded_by.id,
            tenant_id=tenant.id,
            is_active=True,
        ).exists():
            raise ValueError(
                "Recorder does not have an active membership "
                "in the tenant."
            )

        if completed_at is None:
            raise ValueError(
                "Completed time is required."
            )

        if ResearchCompletion.objects.filter(
            protocol_id=protocol.id,
        ).exists():
            raise ValueError(
                "Research completion has already been recorded."
            )

        completion = ResearchCompletion.objects.create(
            tenant=tenant,
            protocol=protocol,
            completed_at=completed_at,
            recorded_by=recorded_by,
        )

        publisher = get_event_publisher()

        publisher.publish(
            ResearchCompleted(
                tenant_id=tenant.id,
                actor_id=recorded_by.id,
                protocol_id=protocol.id,
                research_completion_id=completion.id,
            )
        )

        return completion
