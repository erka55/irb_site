from apps.protocols.enums import ProtocolStatus
from apps.protocols.models import (
    Protocol,
    ProtocolStatusHistory,
)


ALLOWED_TRANSITIONS = {
    ProtocolStatus.DRAFT: [
        ProtocolStatus.SUBMITTED,
    ],
    ProtocolStatus.SUBMITTED: [
        ProtocolStatus.UNDER_REVIEW,
    ],
    ProtocolStatus.UNDER_REVIEW: [
        ProtocolStatus.APPROVED,
        ProtocolStatus.REJECTED,
        ProtocolStatus.REVISIONS_REQUIRED,
    ],
    ProtocolStatus.REVISIONS_REQUIRED: [
        ProtocolStatus.SUBMITTED,
    ],
}


class InvalidTransitionError(Exception):
    pass


class ProtocolWorkflowService:

    @staticmethod
    def can_transition(
        current_status,
        target_status,
    ):
        allowed = ALLOWED_TRANSITIONS.get(
            current_status,
            [],
        )

        return target_status in allowed

    @staticmethod
    def change_status(
        protocol,
        target_status,
        changed_by,
        reason="",
    ):
        if not ProtocolWorkflowService.can_transition(
            protocol.status,
            target_status,
        ):
            raise InvalidTransitionError(
                f"Cannot transition from "
                f"{protocol.status} to "
                f"{target_status}"
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
