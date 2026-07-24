from apps.protocols.services.versioning import (
    ProtocolVersionService,
)

from common.workflow.engine import WorkflowEngine

from apps.protocols.enums import ProtocolStatus
from apps.protocols.models import ProtocolStatusHistory


class ProtocolWorkflowService:

    @staticmethod
    def change_status(
        protocol,
        target_status,
        changed_by,
        reason="",
    ):
        WorkflowEngine.transition(
            current=protocol.status,
            target=target_status,
        )

        previous_status = protocol.status

        protocol.status = target_status
        protocol.save()

        ProtocolStatusHistory.objects.create(
            protocol=protocol,
            from_status=previous_status,
            to_status=target_status,
            changed_by=changed_by,
            reason=reason,
        )

        ProtocolVersionService.create_snapshot(
            protocol=protocol,
            user=changed_by,
        )

        return protocol

    @staticmethod
    def submit(
        protocol,
        changed_by,
    ):
        return ProtocolWorkflowService.change_status(
            protocol=protocol,
            target_status=ProtocolStatus.SUBMITTED,
            changed_by=changed_by,
        )

    @staticmethod
    def start_review(
        protocol,
        changed_by,
    ):
        return ProtocolWorkflowService.change_status(
            protocol=protocol,
            target_status=ProtocolStatus.UNDER_REVIEW,
            changed_by=changed_by,
        )

    @staticmethod
    def approve(
        protocol,
        changed_by,
    ):
        return ProtocolWorkflowService.change_status(
            protocol=protocol,
            target_status=ProtocolStatus.APPROVED,
            changed_by=changed_by,
        )

    @staticmethod
    def reject(
        protocol,
        changed_by,
        reason="",
    ):
        return ProtocolWorkflowService.change_status(
            protocol=protocol,
            target_status=ProtocolStatus.REJECTED,
            changed_by=changed_by,
            reason=reason,
        )

    @staticmethod
    def request_revisions(
        protocol,
        changed_by,
        reason="",
    ):
        return ProtocolWorkflowService.change_status(
            protocol=protocol,
            target_status=ProtocolStatus.REVISIONS_REQUIRED,
            changed_by=changed_by,
            reason=reason,
        )
